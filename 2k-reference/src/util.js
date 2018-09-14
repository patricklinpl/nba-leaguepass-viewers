const gamePayLoad = () => (
  {
    'url': 'scrapeURL',
    'team0': {
      'teamName': '',
      'q1': '',
      'q2': '',
      'q3': '',
      'q4': '',
      'finalScore': '',
      'players': []
    },
    'team1': {
      'teamName': '',
      'q1': '',
      'q2': '',
      'q3': '',
      'q4': '',
      'finalScore': '',
      'players': []
    }
  }
)

const playerPayLoad = () => (
  {
    'name': '',
    'fgm': '',
    '3pm': '',
    'ftm': '',
    'reb': '',
    'ast': '',
    'pf': '',
    'stl': '',
    'tov': '',
    'blk': '',
    'pts': ''
  }
)

export {
  gamePayLoad,
  playerPayLoad
}
