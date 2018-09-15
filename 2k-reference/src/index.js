import 'babel-polyfill'
import fs from 'fs'
import mkdirp from 'mkdirp'
import axios from 'axios'
import cheerio from 'cheerio'
import Promise from 'bluebird'
import { gamePayLoad, playerPayLoad } from './util'

const controller = async () => {
  const container = []
  const matchUrls = await scrapeGameURLs('https://2kleague.nba.com/schedule/')
  await Promise.map(matchUrls, async (gameUrl) => { await scrapeGameStats(gameUrl, container) })
  saveGameMatch(container, ['url', 'teamName', 'q1', 'q2', 'q3', 'q4', 'finalScore', 'name',
    'fgm', '3pm', 'ftm', 'reb', 'ast', 'pf', 'stl', 'tov', 'blk', 'pts'])
}

/**
 * scrapes the unique game URLs
 * @param {string} scrapeURL - schedule url to scrape from
 * @return {array} - an array of unique game urls
 */
const scrapeGameURLs = async (scrapeURL) => {
  const gameURLs = []
  await axios.get(scrapeURL).then((response) => {
    let $ = cheerio.load(response.data)
    $('.schedule-block__team').each((i, elem) => {
      const scrapedURL = $(elem).attr('href')
      if (gameURLs.indexOf(scrapedURL) === -1) {
        gameURLs.push(scrapedURL)
      }
    })
  })
  return gameURLs
}

/**
 * scrapes an individual game's stats
 * @param {string} scrapeURL - match url to scrape from
 * @return {JSOM} - a JSON object that bundles a match's stats together
 */
const scrapeGameStats = async (scrapeURL, container) => {
  const match = gamePayLoad()
  await axios.get(scrapeURL).then(async (response) => {
    match['url'] = scrapeURL
    let $ = cheerio.load(response.data)
    const team0Players = await scrapePlayerGameStats(response.data, '.table.home-players')
    const team1Players = await scrapePlayerGameStats(response.data, '.table.away-players')
    match['date'] = $('.game-header__date').text()
    match['team0']['players'] = team0Players
    match['team1']['players'] = team1Players
    $('.name').each((i, elem) => {
      const boxScoreElement = $(elem).parent()
      match[`team${i}`]['teamName'] = boxScoreElement.find('.name').text().trim()
      boxScoreElement.find('.quarter.q1').each((x, element) => {
        match[`team${i}`][`q${x + 1}`] = $(element).text().trim()
      })
      match[`team${i}`]['finalScore'] = boxScoreElement.find('.quarter.final').text().trim()
    })
    container.push(match)
  })
}

/**
 * scrapes an individual game's stats
 * @param {string} htmlElement - match table html content
 * @param {string} table - css class of the target table
 * @return {array} - an array of JSON objects that bundles a player's individual stats
 */
const scrapePlayerGameStats = async (htmlElement, table) => {
  const players = []
  let $ = cheerio.load(htmlElement)
  $(table).find('tr').each((i, elem) => {
    if ($(elem).find('td[data-type="pts"]').text() !== '') {
      const store = playerPayLoad()
      store['name'] = $(elem).find('td[data-type="ln"]').text()
      store['fgmRatio'] = $(elem).find('td[data-type="fgm"]').text()
      const splitfg = store['fgmRatio'].split('-')
      store['fgm'] = splitfg[0]
      store['fgmPercent'] = parseInt(splitfg[0]) / parseInt(splitfg[1])
      if (store['fgmRatio'] === '0-0') {
        store['fgmPercent'] = 0
      }
      store['3pmRatio'] = $(elem).find('td[data-type="fg3m"]').text()
      const split3pm = store['3pmRatio'].split('-')
      store['3pm'] = split3pm[0]
      store['3pmPercent'] = parseInt(split3pm[0]) / parseInt(split3pm[1])
      if (store['3pmRatio'] === '0-0') {
        store['3pmPercent'] = 0
      }
      store['ftmRatio'] = $(elem).find('td[data-type="ftm"]').text()
      const splitftm = store['ftmRatio'].split('-')
      store['ftm'] = splitftm[0]
      store['ftmPercent'] = parseInt(splitftm[0]) / parseInt(splitftm[1])
      if (store['ftmRatio'] === '0-0') {
        store['ftmPercent'] = 0
      }
      store['reb'] = $(elem).find('td[data-type="reb"]').text()
      store['ast'] = $(elem).find('td[data-type="ast"]').text()
      store['pf'] = $(elem).find('td[data-type="pf"]').text()
      store['stl'] = $(elem).find('td[data-type="stl"]').text()
      store['tov'] = $(elem).find('td[data-type="tov"]').text()
      store['blk'] = $(elem).find('td[data-type="blk"]').text()
      store['pts'] = $(elem).find('td[data-type="pts"]').text()
      console.log(store)
      players.push(store)
    }
  })
  return players
}

/**
 * save game summaries of the conferation as a csv locally
 */
const saveGameMatch = async (match, header) => {
  if (!fs.existsSync('result')) {
    await mkdirp('result', (err) => {
      if (err) console.error(err)
      else console.log('Create path')
    })
  }

  let csv = []
  match.forEach(element => {
    const baseTeam0 = `${element['url']}, ${element['date']}, ${element['team0']['teamName']}, ${element['team0']['q1']}, ${element['team0']['q2']}, ${element['team0']['q3']}, ${element['team0']['q4']}, ${element['team0']['finalScore']},`

    element['team0']['players'].forEach(elem => {
      const player = Object.keys(elem).map(fieldName => JSON.stringify(elem[fieldName])).join(',')
      csv.push(`${baseTeam0}${player}`)
    })

    const baseTeam1 = `${element['url']}, ${element['date']}, ${element['team1']['teamName']}, ${element['team1']['q1']}, ${element['team1']['q2']}, ${element['team1']['q3']}, ${element['team1']['q4']}, ${element['team1']['finalScore']},`

    element['team1']['players'].forEach(elem => {
      const player = Object.keys(elem).map(fieldName => JSON.stringify(elem[fieldName])).join(',')
      csv.push(`${baseTeam1}${player}`)
    })
  })

  csv.join(',')
  csv.unshift(header.join(','))
  csv = csv.join('\r\n')

  await fs.writeFile(`result/match.csv`, csv, 'utf8', (err) => {
    if (err) throw err
    console.log(`The file has been saved!`)
  })
}

controller()
