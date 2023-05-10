var playlist = [];
var currentSong = 0;
var isPlaying = false;
var playbackPosition = 0;
var songList = document.getElementById('song-list');
var urlParams = new URLSearchParams(window.location.search);
var podcast = urlParams.get('podcast');
var podcast = podcast.replace('%20',' ');

console.log(podcast)

if (podcast) {
  filteredSongs = songs.filter(function(song) {
    return song.artist === podcast;
  });
} else {
  // If no artist parameter provided, display all songs
  filteredSongs = songs;
}

filteredSongs.sort(function(a, b) {
  return new Date(b.date) - new Date(a.date);
});

for (var i = 0; i < filteredSongs.length; i++) {
    (function(index) {
    var container = document.createElement('div');
    var song = filteredSongs[i];
    var artistElement = document.createElement('p');
    var titleElement = document.createElement('p');

    artistElement.textContent = song.artist;
    artistElement.classList.add('artist');
    
    titleElement.textContent = song.date + ' - ' + song.name;
    titleElement.classList.add('details');

	container.setAttribute('class', 'song');
	container.setAttribute('onClick', 'nowPlaying()');
    container.appendChild(artistElement);
    container.appendChild(titleElement);
    container.addEventListener('click', function() {
	playSong(index);
    });
	songList.appendChild(container);
    })(i);
};

function nowPlaying() {
    var now_playing_div = document.getElementById("now-playing");
    var click_event = event.currentTarget;
    if (now_playing_div) {
	now_playing_div.removeAttribute('id');
    };
    click_event.id = 'now-playing';
}; 
var player = new Howl({
    src: [filteredSongs[currentSong].url],
    html5: true,
    onload: function() {
	updateMetadata();
    }
});

function updateMetadata() {
  var currentSongData = filteredSongs[currentSong];
  document.getElementById('song-title').textContent = currentSongData.name;
  document.getElementById('song-image').src = currentSongData.cover_art_url;
};

function updateProgressBar() {
  var progress = player.seek() / player.duration() * 100; // Calculate the progress percentage
  var progressBar = document.getElementById('progress-bar');
  progressBar.style.width = progress + '%'; // Set the width of the progress bar element
}

function playNext() {
    currentSong++;
    if (currentSong >= filteredSongs.length) {
	currentSong = 0; // Start from the beginning if reached the end
    };
    playCurrentSong(playbackPosition);
};

function playPrevious() {
  currentSong--;
  if (currentSong < 0) {
    currentSong = filteredSongs.length - 1; // Go to the last song if reached the beginning
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
	src: [filteredSongs[currentSong].url],
	html5: true,
	onload: function() {
	    updateMetadata();
	    if (!player.playing()) {
		player.play(); // Start playing the new song if it's not already playing
	    }
	},
	onplay: function() {
	    updateProgressBar();
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
