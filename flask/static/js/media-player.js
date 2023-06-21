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
    var playedElement = document.createElement('p')

    artistElement.textContent = song.artist;
    artistElement.classList.add('artist');

    titleElement.textContent = song.date + ' - ' + song.name;
    titleElement.classList.add('details');

    playedElement.textContent = song.played;

    container.setAttribute('class', 'song');
    container.setAttribute('onClick', 'nowPlaying()');
    container.appendChild(artistElement);
    container.appendChild(titleElement);
    container.appendChild(playedElement);
    container.addEventListener('click', function() {
      playSong(index);
      requestAnimationFrame(step);
    });
  	songList.appendChild(container);
    // MediaSession stuff for phones
    if ("mediaSession" in navigator) {
    navigator.mediaSession.metadata = new MediaMetadata({
      title: song.name,
      artwork:[{ src: song.cover_art_url, sizes: '512x512', type: 'image/jpeg' }] 
    })
    navigator.mediaSession.setActionHandler("play",() => {
      playButton()  
    })
    navigator.mediaSession.setActionHandler("pause",() => {
      pauseButton()
    })
    navigator.mediaSession.setActionHandler("seekbackward",() => {
      skipBackward()
    })
    navigator.mediaSession.setActionHandler("seekforward",() => {
      skipForward()
    })
    navigator.mediaSession.setActionHandler("nexttrack", () => {
      playNext()
    })
    navigator.mediaSession.setActionHandler("previoustrack", () => {
      playPrevious()
    })
    navigator.mediaSession.setActionHandler("seekto", () => {
      seekBar();
    })
  };
  })(i);
};

function checkPlayed(value) {
  return value.played == "1"
};

function hidePlayed() {
  var song_elements = document.getElementsByClassName('song');
  for (var i = song_elements.length - 1; i >= 0; i--) {
    var played_element = song_elements[i].querySelector('.played');
    console.log(played_element.textContent);
    if (played_element.textContent.includes("1")) {
      song_elements[i].remove();
    } else {
      console.log("Not played")  
    }
  }
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
      timeSpan();
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
    player.play()
};

function playPrevious() {
  currentSong--;
  if (currentSong < 0) {
    currentSong = filteredSongs.length - 1; // Go to the last song if reached the beginning
  };
  playCurrentSong(playbackPosition);
  player.play();
};

function playSong(songIndex) {
    currentSong = songIndex;
    playCurrentSong(playbackPosition);
    speedSelect.value = '1';
    player.play();
}

function playCurrentSong(playbackPosition) {
    player.stop(); // Stop the currently playing song
    player.unload(); // Unload the current song
    player = new Howl({
  	src: [filteredSongs[currentSong].url],
	    html5: true,
	    onload: function() {
	        updateMetadata();
        },
        onplay: function() {
          updateMetadata()
          requestAnimationFrame(step)
          timeSpan()
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

function skipForward() {
  playbackPosition = player.seek();
  forwardPosition = playbackPosition + 30;
  player.seek(forwardPosition);
  console.log("Skipping From ", playbackPosition, " To ", forwardPosition);
}

function skipBackward() {
  playbackPosition = player.seek();
  backwardPosition = playbackPosition - 30;
  player.seek(backwardPosition);
  console.log("Skipping From ", playbackPosition, " To ", backwardPosition);
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
  var skipSeconds = duration * ( percentage / 100 );
  console.log(skipSeconds);
  player.seek(skipSeconds);
  player.play();
}

speedSelect.addEventListener('change', function() {
  var selectedSpeed = parseFloat(speedSelect.value);
  changePlaybackSpeed(selectedSpeed);
});

function timeSpan() {
  var currentTime = setInterval(player.seek(), 500)
  var duration = player.duration();
  var timeElement = document.getElementById("time");
  timeElement.innerHTML = currentTime + " / " + duration;
}
