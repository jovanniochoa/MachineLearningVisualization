
    // Set the start and end dates (change them to your desired dates)
    var startDate = new Date("2022-05-01T00:00:00Z").getTime();
    var endDate = new Date("2023-06-30T23:59:59Z").getTime();
    
    // Update the timer every second
    var timer = setInterval(function() {
      // Get current date and time
      var now = new Date().getTime();
      
      // Calculate the remaining time
      var remainingTime = endDate - now;
      var elapsedTime = now - startDate;
      
      // Calculate the progress percentage
      var progressPercentage = (elapsedTime / (endDate - startDate)) * 100;
      progressPercentage = Math.min(progressPercentage, 100); // Ensure the progress doesn't exceed 100%
      
      // Update the loading progress and display the percentage
      document.getElementById("progress").innerText = Math.round(progressPercentage) + "%";
      document.getElementById("progress").style.width = progressPercentage + "%";
      
      // Stop the timer when the countdown is over
      if (remainingTime <= 0) {
        clearInterval(timer);
        document.getElementById("progress").innerText = "100%";
        document.getElementById("progress").style.width = "100%";
      }
      
      // Calculate the days, hours, minutes, and seconds
      var days = Math.floor(remainingTime / (1000 * 60 * 60 * 24));
      var hours = Math.floor((remainingTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      var minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
      var seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);
      
      // Update the timer elements
      document.getElementById("days").innerText = days.toString().padStart(2, "0");
      document.getElementById("hours").innerText = hours.toString().padStart(2, "0");
      document.getElementById("minutes").innerText = minutes.toString().padStart(2, "0");
      document.getElementById("seconds").innerText = seconds.toString().padStart(2, "0");
    }, 1000);
