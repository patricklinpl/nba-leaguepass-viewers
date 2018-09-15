const gamePayLoad = () => (
  {
    'url': '',
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
    'fgmRatio': '',
    'fgm': '',
    'fgmPercent': '',
    '3pmRatio': '',
    '3pm': '',
    '3pmPercent': '',
    'ftmRatio': '',
    'ftm': '',
    'ftmPercent': '',
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
