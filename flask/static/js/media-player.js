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
    playedElement.classList.add('played')

    container.setAttribute('class', 'song');
    container.setAttribute('onClick', 'nowPlaying()');
    container.appendChild(artistElement);
    container.appendChild(titleElement);
    container.appendChild(playedElement);
    container.addEventListener('click', function() {
      playSong(index);
      requestAnimationFrame(step);
      mediaSessionUpdateMeta()
    });
  	songList.appendChild(container);
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
  var currentSongName = currentSongData.name;
  var currentSongImage = currentSongData.cover_art_url;
  document.getElementById('song-title').textContent = currentSongName;
  document.getElementById('song-image').src = currentSongImage;
  podcastDescription.textContent = currentSongData.description;
  return currentSongName, currentSongImage
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
        mediaSessionUpdateMeta()
      },
      onplay: function() {
        var podName = filteredSongs[currentSong].name
        currentTime = localStorage.getItem(podName) || 0;
        player.seek(currentTime)
        mediaSessionUpdateMeta()
        updateMetadata()
        requestAnimationFrame(step)
        setInterval(timeSpan, 500)
        setInterval(storeTime, 10000)
      },
      onend: function(episode_title) {
        var currentSongData = filteredSongs[currentSong];
        var episode_title = document.getElementById('song-title').textContent = currentSongData.name;
        episodePlayedDB(episode_title)
      }
    }
  )
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

function getCurrentTime() {
  var seek = player.seek() || 0;
  var currentMinutes = Math.floor(seek / 60);
  var currentSeconds = Math.trunc(seek % 60);
  var currentHours = Math.floor(currentMinutes / 60);
  var currentMinutes = currentMinutes % 60;
  var currentTime = currentHours + ":" + currentMinutes + ":" + currentSeconds;
  return currentTime
}

function getTotalTime() {
  var totalTime = player.duration();
  var totalMinutes = Math.floor(totalTime / 60);
  var totalSeconds = Math.trunc(totalTime % 60);
  var totalHours = Math.floor(totalMinutes / 60);
  var totalMinutes = totalMinutes % 60;
  var totalDuration = totalHours + ":" + totalMinutes + ":" + totalSeconds
  return totalDuration
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
}

speedSelect.addEventListener('change', function() {
  var selectedSpeed = parseFloat(speedSelect.value);
  changePlaybackSpeed(selectedSpeed);
});

function timeSpan() {
  var currentTime = getCurrentTime();
  var totalTime = getTotalTime(); 
  var currentTimeElement = document.getElementById("current-time");
  var totalTimeElement = document.getElementById("total-time");
  currentTimeElement.innerHTML = currentTime ;
  totalTimeElement.innerHTML = totalTime;
}

function storeTime() {
  var podName = filteredSongs[currentSong].name
  var currentTime = player.seek()
  localStorage.removeItem(podName)
  localStorage.setItem(podName, currentTime)
}

function mediaSessionUpdateMeta() {
  var currentSongData = filteredSongs[currentSong];
  var currentSongName = currentSongData.name;
  var currentSongImage = currentSongData.cover_art_url;
  var currentSongArtist = currentSongData.artist;
  navigator.mediaSession.metadata = new MediaMetadata({
    title: currentSongName,
    artist: currentSongArtist,
    artwork:[{ src: currentSongImage, sizes: '512x512', type: 'image/jpeg' }] 
  })
  document.title = currentSongArtist + " - " + currentSongName;
}

// MediaSession stuff for phones
if ("mediaSession" in navigator) {
  mediaSessionUpdateMeta();
  navigator.mediaSession.setActionHandler("play",() => {
    playButton()
    mediaSessionUpdateMeta()
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
    mediaSessionUpdateMeta()
  })
  navigator.mediaSession.setActionHandler("previoustrack", () => {
    playPrevious()
    mediaSessionUpdateMeta()
  })
  navigator.mediaSession.setActionHandler("seekto", (details) => {
    player.seek(details.seekTime);
  })}