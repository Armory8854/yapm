var playlist = [];
var currentSong = 0;
var isPlaying = false;
var playbackPosition = 0;
var songList = document.getElementById('song-list');

for (var i = 0; i < songs.length; i++) {
    var container = document.createElement('div');
    var song = songs[i];
    var artistElement = document.createElement('p');
    var titleElement = document.createElement('p');

    artistElement.textContent = song.artist;
    artistElement.classList.add('artist');
    
    titleElement.textContent = song.date + ' - ' + song.name;
    titleElement.classList.add('details');
    
    container.setAttribute('class', 'song' + i);
    container.appendChild(artistElement);
    container.appendChild(titleElement);
  
    container.addEventListener('click', function() {
	playSong(i);
    });
  
    songList.appendChild(container);
};

var player = new Howl({
    src: [songs[currentSong].url],
    html5: true,
    onload: function() {
	updateMetadata();
    }
});

function updateMetadata() {
  var currentSongData = songs[currentSong];
  document.getElementById('song-title').textContent = currentSongData.name;
  document.getElementById('song-image').src = currentSongData.cover_art_url;
};

function playNext() {
    currentSong++;
    if (currentSong >= songs.length) {
	currentSong = 0; // Start from the beginning if reached the end
    };
    playCurrentSong(playbackPosition);
};

function playPrevious() {
  currentSong--;
  if (currentSong < 0) {
    currentSong = songs.length - 1; // Go to the last song if reached the beginning
  };
  playCurrentSong(playbackPosition);
};

function playSong(songIndex) {
    currentSong = songIndex;
    playCurrentSong(playbackPosition);
}

function playCurrentSong(playbackPosition) {
  player.stop(); // Stop the currently playing song
  player.unload(); // Unload the current song
 player = new Howl({
    src: [songs[currentSong].url],
    html5: true,
    onload: function() {
	updateMetadata();
	if (!player.playing()) {
        player.play(); // Start playing the new song if it's not already playing
      }
    }
  });
}

function playButton() {
    player.seek(playbackPosition);
    player.play();
}

function pauseButton() {
    playbackPosition = player.seek();
    player.pause();
}

function togglePlay() {
  if (player) {
    if (player.playing()) {
      playbackPosition = player.seek();
      player.pause();
    } else {
      player.seek(playbackPosition);
      player.play();
    }
  }
}
