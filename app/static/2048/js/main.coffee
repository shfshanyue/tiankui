class Game 
  constructor: ->
    @start()

  start: ->
    if localStorage && localStorage.getItem('tiles')
      @score = parseInt localStorage.getItem('score')
      @tiles = JSON.parse localStorage.getItem('tiles')
      $('.score').text @score
      $('.score-best').text localStorage.getItem('bestScore')
      for i in [0...4]
        for j in [0...4]
          @addTile(i, j, @tiles[i][j])
    else
      $('.score').text 0  
      if localStorage.getItem('bestScore')
        $('.score-best').text localStorage.getItem('bestScore')
      $('.tile').remove()

      @score = 0
      @over = false
      @tiles = []
      for i in [0...4]
        @tiles[i] = []
        for j in [0...4]
          @tiles[i][j] = 0
      @generateTile()
      @generateTile() 
    return 

  getEnableTiles: ->
    enableTiles = []
    for i in [0...4]
      for j in [0...4]
        if @tiles[i][j] == 0
          enableTiles.push({x:i, y:j})
    enableTiles

  addTile: (i, j, value) ->
    if value
      tileText = "<div class='tile tile-#{value} tile-pos-#{i}-#{j} tile-new'><div class='tile-inner'>#{value}</div></div>"
      $('.tile-container').append tileText

  generateTile: ->
    enableTiles = @getEnableTiles()
    len = enableTiles.length
    tile = enableTiles[Math.floor(Math.random() * len)]
    @tiles[tile.x][tile.y] = 2
    @addTile(tile.x, tile.y, 2)
    return

  findTile: (tile, vertex) ->
    merge = 0
    {x, y} = tile
    loop
      [pre_x, pre_y] = [x, y]
      [x, y] = [pre_x+vertex.x, pre_y+vertex.y]
      break unless x < 4 and x >=0 and y < 4 and y >= 0 and @tiles[x][y] == 0
    to = {x:pre_x, y:pre_y}
    if x < 4 and x >=0 and y < 4 and y >= 0 and @tiles[x][y] == @tiles[tile.x][tile.y] and @used[x][y] == 0
      merge = @tiles[x][y]
      to = {x:x, y:y}
      @used[x][y] = 1
    {to: to, merge: merge}

  moveSingleTile: (tile, vertex) ->
    isMove = false
    score_add = 0
    {to, merge
    } = @findTile(tile, vertex)
    if tile.x != to.x or tile.y != to.y
      @moveTileAct(tile, to, merge)
      isMove = true
    {isMove: isMove, score_add: merge}

  moveTileAct: (fromTile, toTile, merge) ->
    {x: m, y: n} = toTile
    {x: i, y: j} = fromTile
    @tiles[m][n] = @tiles[i][j]
    @tiles[i][j] = 0
    p = $(".tile-pos-#{i}-#{j}")
    if merge 
      @tiles[m][n] = merge * 2
      $(".tile-pos-#{m}-#{n}").remove()
      p.addClass("tile-merge tile-#{@tiles[m][n]}")
      $('.tile-inner', p).text(@tiles[m][n])
    p.removeClass("tile-pos-#{i}-#{j}").addClass("tile-pos-#{m}-#{n}")

  moveVertex: (vertex) ->
    canMove = false
    score_sum = 0
    grids = {x: [], y: []}
    for i in [0...4]
      grids.x.push i
      grids.y.push i
    if vertex.y == 1
      grids.y.reverse()
    if vertex.x == 1
      grids.x.reverse()
      
    @used = []
    for i in [0...4]
      @used[i] = []
      for j in [0...4]
        @used[i][j] = 0
    
    for i in grids.x
      for j in grids.y
        if @tiles[i][j] != 0
          {isMove, score_add} = @moveSingleTile({x:i, y:j}, vertex)
          canMove = canMove or isMove
          score_sum = score_add + score_sum
    {score_sum: score_sum, canMove: canMove}

  move: (keyCode) ->
    vertexs = [{x:0, y:-1}, {x:-1, y:0}, {x:0, y:1}, {x:1, y:0}]

    switch keyCode
      when 37
        vertex = vertexs[0]
      when 38
        vertex = vertexs[1]
      when 39
        vertex = vertexs[2]
      when 40
        vertex = vertexs[3]

    self = @
    window.requestAnimationFrame () ->
      {score_sum, canMove} = self.moveVertex(vertex)
      if canMove
        self.generateTile() 
        self.updateScore score_sum if score_sum
      else
        self.isGameover()
      
      localStorage.setItem 'tiles', JSON.stringify(self.tiles) 
      return 

    return

  updateScore: (score_add) ->
    @score = @score + score_add
    $('.score-count').text @score
    $('.score-add').remove()
    $('.score-panel').append '<div class="score-add"></div>'
    $('.score-add').text "+#{score_add}"

    localStorage.setItem('score', @score)
    if @score > localStorage.getItem('bestScore')
      localStorage.setItem('bestScore', @score) 
      $('.score-best').text @score
    return

  isGameover: ->
    len = @getEnableTiles().length
    if len != 0
      return
    for i in [0...4]
      for j in [0...4]
        if (j < 3 and @tiles[i][j] == @tiles[i][j+1]) or (i < 3 and @tiles[i][j] == @tiles[i+1][j])
          return
    $('.over-container').addClass 'active'
    @over = true

    return

game = new Game()
$(document).on 'keydown', (event) ->
  event.preventDefault()
  if not game.over and event.keyCode in [37, 38, 39, 40]
    game.move(event.keyCode)
  return

$('.start').on 'click', (event) ->
  $('.over-container').removeClass 'active'
  localStorage.removeItem 'score'
  localStorage.removeItem 'tiles'
  game.start()
  return



