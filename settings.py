screen_width = 1000
screen_height = 600
fps = 60

colors = {
  'sky':  '#72D7EE',
  'tree': '#005108',
  'fog':  '#005108',
  'light':  { 'road': '#6B6B6B', 'grass': '#10AA10', 'rumble': '#555555', 'lane': '#CCCCCC'},
  'dark':   { 'road': '#696969', 'grass': '#009A00', 'rumble': '#BBBBBB', 'lane': '#696969'},
  'start':  { 'road': 'white',   'grass': 'white',   'rumble': 'white'},
  'finish': { 'road': 'black',   'grass': 'black',   'rumble': 'black' }
}


path_bg = 'images/background/'
path_sp = 'images/sprites/'
images = {
    'background': {'hills':path_bg+'hills.png','sky': path_bg+'sky.png', 'trees': path_bg+'trees.png'},
    'player': {'right': path_sp+'player_right.png', 'left': path_sp+'player_left.png', 'reto': path_sp+'player_straight.png'}
}

