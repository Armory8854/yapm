// Organize vars here - currently very jank and unorgainzed
var currentSong = 0;
var isPlaying = false;
var playbackPosition = 0;
var songList = document.getElementById('song-list');
var urlParams = new URLSearchParams(window.location.search);
var podcast = urlParams.get('podcast');
var podcast = podcast.replace('%20',' ');
var speedSelect = document.getElementById('speed-select');
var podcastDescription = document.getElementById('description-full-text')
var progress = document.getElementById('progress-bar')
var progressBarContainer = document.getElementById('progress-bar-container')
var duration = 0;

// Add event listeners here, mainly for seek bar
progressBarContainer.addEventListener('click', seekBar);

function changePlaybackSpeed(speed) {
  player.rate(speed);
};

function episodePlayedDB(episode_title) {
  var postData = {
    episode_title: episode_title,
    episode_played: 1
  };
  var jsonData = JSON.stringify(postData);
  fetch('/episode-played', {
    method: 'POST',
    headers: {
      'Content-Type':'application/json'
    },
    body: jsonData
  });
  console.log(episode_title + 'Added to DB');
};

if (podcast) {
  filteredSongs = songs.filter(function(song) {
    return song.artist === podcast;
  });
} else {
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
      requestAnimationFrame(step);
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
    onplay: function() {
      updateMetadata();
    	requestAnimationFrame(step);
    },
    onload: function() {
      updateMetadata();
    },
});

function updateMetadata() {
  var currentSongData = filteredSongs[currentSong];
  document.getElementById('song-title').textContent = currentSongData.name;
  document.getElementById('song-image').src = currentSongData.cover_art_url;
  podcastDescription.textContent = currentSongData.description;
};


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
    speedSelect.value = '1';
}

function playCurrentSong(playbackPosition) {
    player.stop(); // Stop the currently playing song
    player.unload(); // Unload the current song
    player = new Howl({
  	src: [filteredSongs[currentSong].url],
	    html5: true,
	    onload: function() {
        var duration = player.duration();
        console.log('Song Duration: ' + duration);
	      updateMetadata();
          if (!player.playing()) {
            player.play();
            player.rate(1);
          }
        },
        onplay: function() {
          updateMetadata()
          requestAnimationFrame(step)
        },
        onend: function(episode_title) {
          var currentSongData = filteredSongs[currentSong];
          var episode_title = document.getElementById('song-title').textContent = currentSongData.name;
          episodePlayedDB(episode_title)
        }
      });
    }

function pauseButton() {
    playbackPosition = player.seek();
    console.log("playback position is", playbackPosition)
    player.pause();
}

function playButton() {
    player.seek(playbackPosition);
    player.play();
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

function step() {
  var seek = player.seek() || 0;
  progress.style.width = (((seek / player.duration()) * 100) || 0) + '%';
  if (player.playing()) {
      requestAnimationFrame(step);
  }
}


function seekBar(event) {
  var duration = player.duration();
  var offset = event.clientX - progressBarContainer.offsetLeft;
  var containerWidth = progressBarContainer.clientWidth;
  var percentage = (offset / containerWidth) * 100;
  progress.style.width = percentage + '%';
  var skipPercent = duration * ( percentage / 100 );
  console.log(skipPercent);
  player.seek(skipPercent);
  player.play();
}

speedSelect.addEventListener('change', function() {
  var selectedSpeed = parseFloat(speedSelect.value);
  changePlaybackSpeed(selectedSpeed);
});
