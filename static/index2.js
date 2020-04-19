var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

socket.on("connect", () => {
  document.querySelectorAll("button").forEach(button => {
      button.onclick = () => {
          const selection = button.dataset.vote;
          socket.emit('submit vote', {"selection" : selection})
      };
  });
})
