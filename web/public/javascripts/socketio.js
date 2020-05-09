$(document).ready(function() {
  var socket = io.connect('localhost:3000');
  socket.emit('joinRoom', {roomName: 'room1', msg: 'test'});
  socket.emit('messages', 'Hello from the client');
  socket.on('messages', function (data) {
      terminal.replaceRange(data, CodeMirror.Pos(terminal.lastLine()))
  });
});
