import 'babel-polyfill'
import axios from 'axios'
import cheerio from 'cheerio'
import Promise from 'bluebird'
import { gamePayLoad, playerPayLoad } from './util'

/**
 * @return {array} - an array of game stats
 */
const controller = async () => {
  const container = []
  const matchUrls = await scrapeGameURLs('https://2kleague.nba.com/schedule/')
  await Promise.map(matchUrls, async (gameUrl) => { await scrapeGameStats(gameUrl, container) })
  return container
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
    let $ = cheerio.load(response.data)
    const team0Players = await scrapePlayerGameStats(response.data, '.table.home-players')
    const team1Players = await scrapePlayerGameStats(response.data, '.table.away-players')
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
    const store = playerPayLoad()
    store['name'] = $(elem).find('td[data-type="ln"]').text()
    store['fgm'] = $(elem).find('td[data-type="fgm"]').text()
    store['3pm'] = $(elem).find('td[data-type="fg3m"]').text()
    store['ftm'] = $(elem).find('td[data-type="ftm"]').text()
    store['reb'] = $(elem).find('td[data-type="reb"]').text()
    store['ast'] = $(elem).find('td[data-type="ast"]').text()
    store['pf'] = $(elem).find('td[data-type="pf"]').text()
    store['stl'] = $(elem).find('td[data-type="stl"]').text()
    store['tov'] = $(elem).find('td[data-type="tov"]').text()
    store['blk'] = $(elem).find('td[data-type="blk"]').text()
    store['pts'] = $(elem).find('td[data-type="pts"]').text()
    if (store['pts'] !== '') {
      players.push(store)
    }
  })
  return players
}

controller()
