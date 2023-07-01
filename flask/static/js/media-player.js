// Organize vars here - currently very jank and unorgainzed
var currentSong = 0;
var isPlaying = false;
var playbackPosition = 0;
var currentChapterIndex = 0;
var pausedPosition = 0;
var songList = document.getElementById('song-list');
var urlParams = new URLSearchParams(window.location.search);
var podcast = urlParams.get('podcast');
var podcast = podcast.replace('%20',' ');
var speedSelect = document.getElementById('speed-select');
var podcastDescription = document.getElementById('description-full-text')
var progress = document.getElementById('progress-bar')
var progressBarContainer = document.getElementById('progress-bar-container')
var duration = 0;
var episodeChapters = ""

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
    onload: async function() {
      playbackPosition = await getCurrentTimeDB()
      episodeChapters = await getEpisodeChapters()
      console.log(episodeChapters)
      mediaSessionUpdateMeta()
      updateChapter(playbackPosition)
      updateMetadata();
      timeSpan();
    },
    onplay: function() {
      requestAnimationFrame(step);
      requestAnimationFrame(chapterSpanFunction)
      updateChapter(playbackPosition)
      intervalId = setInterval(storeTime, 1000);
    },
    onpause: function() {
      pausedPosition = player.seek();
      updateChapter(pausedPosition);
      clearInterval(intervalId)
    }
});

function updateMetadata() {
  var currentSongData = filteredSongs[currentSong];
  var currentSongName = currentSongData.name;
  var currentSongImage = currentSongData.cover_art_url;

  const parser = new DOMParser();
  const episodeDescription = parser.parseFromString(currentSongData.description, 'text/html');
  document.getElementById('song-title').textContent = currentSongName;
  document.getElementById('song-image').src = currentSongImage;
  podcastDescription.innerHTML = episodeDescription.body.innerText;
  return currentSongName, currentSongImage
};


function playNext() {
    currentSong++;
    if (currentSong >= filteredSongs.length) {
	    currentSong = 0; // Start from the beginning if reached the end
    };
    playCurrentSong();
    player.play()
};

function playPrevious() {
  currentSong--;
  if (currentSong < 0) {
    currentSong = filteredSongs.length - 1; // Go to the last song if reached the beginning
  };
  playCurrentSong();
  player.play();
};

function playSong(songIndex) {
    currentSong = songIndex;
    playCurrentSong(playbackPosition);
    speedSelect.value = '1';
}

async function playCurrentSong(playbackPosition) {
    player.stop(); // Stop the currently playing song
    player.unload(); // Unload the current song
    playbackPosition = await getCurrentTimeDB()
    episodeChapters = await getEpisodeChapters()
    player = new Howl({
  	src: [filteredSongs[currentSong].url],
	    html5: true,
	    onload: function() {
        player.seek(playbackPosition);        
        updateMetadata();
        mediaSessionUpdateMeta()
        player.play()
        updateChapter(playbackPosition)
      },
      onplay: function() {
        mediaSessionUpdateMeta()
        requestAnimationFrame(step)
        requestAnimationFrame(timeSpan)
        requestAnimationFrame(chapterSpanFunction)
        intervalId = setInterval(storeTime, 1000)
      },
      onpause: function() {
        pausedPosition = player.seek();
        clearInterval(intervalId) 
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
    player.pause();
}

function playButton(playbackPosition) {
    player.seek(playbackPosition);
    player.play();
}

function skipForward() {
  playbackPosition = player.seek();
  forwardPosition = playbackPosition + 30;
  player.seek(forwardPosition);
}

function skipBackward() {
  playbackPosition = player.seek();
  backwardPosition = playbackPosition - 30;
  player.seek(backwardPosition);
}

function togglePlay() {
  if (player) {
    if (player.playing()) {
      player.pause();
    } else {
      if (pausedPosition > 0) {
        player.seek(pausedPosition);
        player.play()
      } else {
        player.seek(playbackPosition)
        player.play()
      }
    }
  }
}

function getCurrentTimeSpan() {
  var seek = player.seek() || 0;
  var currentMinutes = Math.floor(seek / 60);
  var currentSeconds = Math.trunc(seek % 60);
  var currentHours = Math.floor(currentMinutes / 60);
  var currentMinutes = currentMinutes % 60;
  var currentTimeSpan = currentHours + ":" + currentMinutes + ":" + currentSeconds;
  return currentTimeSpan
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
  player.seek(skipSeconds);
  pausedPosition = player.seek()
  updateChapter(skipSeconds);
}

speedSelect.addEventListener('change', function() {
  var selectedSpeed = parseFloat(speedSelect.value);
  changePlaybackSpeed(selectedSpeed);
});

function timeSpan() {
  var currentTimeSpan = getCurrentTimeSpan();
  var totalTime = getTotalTime(); 
  var currentTimeElement = document.getElementById("current-time");
  var totalTimeElement = document.getElementById("total-time");
  currentTimeElement.innerHTML = currentTimeSpan ;
  totalTimeElement.innerHTML = totalTime;
  requestAnimationFrame(timeSpan)
}

function storeTime() {
  var episode_title = filteredSongs[currentSong].name
  var currentTimeStore = player.seek()
  var postData = {
    episode_title: episode_title,
    current_time: currentTimeStore 
  }
  var jsonData = JSON.stringify(postData);
  if (player.playing) {
    fetch('/current-time', {
      method: 'POST',
      headers: {
        'Content-Type':'application/json'
      },
      body: jsonData
    })
  } else {
    return 
  }
}

async function getCurrentTimeDB() {
  var episode_title = filteredSongs[currentSong].name
  var url = '/current-time?episode_title=' + encodeURIComponent(episode_title);
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const myJson = await response.json();
    playbackPosition = myJson['current_time_get']
    return playbackPosition 
  } catch (error) {
    console.error(error);
    throw error;
  }
}
async function getEpisodeChapters() {
  var episode_title = filteredSongs[currentSong].name
  var url = '/episode-metadata?query=chapters&episode-title=' + encodeURIComponent(episode_title);
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    const chaptersJson = await response.json();
    episodeChapters = chaptersJson['episode_chapters']
    return episodeChapters 
  } catch (error) {
    console.error(error);
    throw error;
  }
}

function nextChapterSkip() {
  currentChapterIndex++
  var chaptersLength = episodeChapters.length
  if (currentChapterIndex >= chaptersLength) {
    currentChapterIndex = chaptersLength - 1
  }
  var startTime = episodeChapters[currentChapterIndex]['startTime']
  console.log(currentChapterIndex)
  player.seek(startTime)
  player.play()
}

function previousChapterSkip() {
  currentChapterIndex--
  if (currentChapterIndex <= 0) {
    currentChapterIndex = 0 
  }
  var startTime = episodeChapters[currentChapterIndex]['startTime']
  console.log(currentChapterIndex)
  player.seek(startTime)
  player.play()
}

function chapterSpanFunction() {
  chapterSpan = document.getElementById("chapter-name")
  if (episodeChapters.length > 0) {
    chapterSpan.innerHTML = "Chapter " + currentChapterIndex + ": " + episodeChapters[currentChapterIndex]['title']
    requestAnimationFrame(chapterSpanFunction)
  } else {
    chapterSpan.innerHTML = "No Chapters Available"   
    requestAnimationFrame(chapterSpanFunction)
  }
}

function updateChapter(skipSeconds) {
  chaptersLength = episodeChapters.length
  chapterSpan = document.getElementById("chapter-name")
  if (chaptersLength > 0) {
    for (var i = 0; i < chaptersLength; i++) {
      if (skipSeconds >= episodeChapters[i]['startTime']) {
        currentChapterIndex = i;
        chapterSpan.innerHTML = "Chapter " + currentChapterIndex + ": " + episodeChapters[i]['title']
      } else {
        break
      }
    }
  }
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
  })
}