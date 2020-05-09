var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var app = express();
var server = require('http').createServer(app);
var io = require('socket.io')(server);

var indexRouter = require('./routes/index');

var PORT = process.env.PORT || 3000;

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

io.on('connection', function(client) {
  console.log(`A user is connected. Client id: ${client.id}`);
  client.on('joinRoom', function(room) {
    let roomName = room.roomName;
    client.join(roomName);
    console.log(`room number ${roomName}`);
    client.on('messages', function(msg) {
      io.to(roomName).emit('messages', 'Hello from the server.');
    });
  });
});
server.listen(PORT, function(){
  console.log(`Local Tester running at http://localhost:${PORT}`);
});

module.exports = app;
