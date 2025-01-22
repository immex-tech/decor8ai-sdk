import { startVirtualStaging } from 'backend/decor8ai';
import wixRealtime from 'wix-realtime';
import { v4 as v4uuid } from 'uuid';

$w.onReady ( () => {
	$w('#errorMessage').hide ();
	$w('#progressIndicator').hide();

$w("#roomTypeDropdown").options = [
    { label: "Living Room", value: "LIVINGROOM" },
    { label: "Kitchen", value: "KITCHEN" },
    { label: "Dining Room", value: "DININGROOM" },
    { label: "Bedroom", value: "BEDROOM" },
    { label: "Bathroom", value: "BATHROOM" },
    { label: "Kids Room", value: "KIDSROOM" },
    { label: "Family Room", value: "FAMILYROOM" },
    { label: "Reading Nook", value: "READINGNOOK" },
    { label: "Sunroom", value: "SUNROOM" },
    { label: "Walk-In Closet", value: "WALKINCLOSET" },
    { label: "Mud Room", value: "MUDROOM" },
    { label: "Toy Room", value: "TOYROOM" },
    { label: "Home Office", value: "OFFICE" },
    { label: "Foyer", value: "FOYER" },
    { label: "Powder Room", value: "POWDERROOM" },
    { label: "Laundry Room", value: "LAUNDRYROOM" },
    { label: "Home Gym", value: "GYM" },
    { label: "Basement", value: "BASEMENT" },
    { label: "Garage", value: "GARAGE" },
    { label: "Balcony", value: "BALCONY" },
    { label: "Urban Cafe", value: "CAFE" },
    { label: "Home Bar", value: "HOMEBAR" },
    { label: "Study Room", value: "STUDY_ROOM" },
    { label: "Front Porch", value: "FRONT_PORCH" },
    { label: "Back Porch", value: "BACK_PORCH" },
    { label: "Back Patio", value: "BACK_PATIO" },
];  

$w("#designStyleDropdown").options = [
    { label: "Minimalist", value: "MINIMALIST" },
    { label: "Scandinavian", value: "SCANDINAVIAN" },
    { label: "Industrial", value: "INDUSTRIAL" },
    { label: "Boho", value: "BOHO" },
    { label: "Traditional", value: "TRADITIONAL" },
    { label: "Art Deco", value: "ARTDECO" },
    { label: "Mid-Century Modern", value: "MIDCENTURYMODERN" },
    { label: "Coastal", value: "COASTAL" },
    { label: "Tropical", value: "TROPICAL" },
    { label: "Eclectic", value: "ECLECTIC" },
    { label: "Contemporary", value: "CONTEMPORARY" },
    { label: "French Country", value: "FRENCHCOUNTRY" },
    { label: "Rustic", value: "RUSTIC" },
    { label: "Shabby Chic", value: "SHABBYCHIC" },
    { label: "Vintage", value: "VINTAGE" },
    { label: "Country", value: "COUNTRY" },
    { label: "Modern", value: "MODERN" },
    { label: "IKEA", value: "IKEA" },
    { label: "Pottery Barn", value: "POTTERYBARN" },
    { label: "West Elm Modern", value: "WESTELMMODERN" },
    { label: "Asian Zen", value: "ASIAN_ZEN" },
    { label: "Hollywood Regency", value: "HOLLYWOODREGENCY" },
    { label: "Bauhaus", value: "BAUHAUS" },
    { label: "Mediterranean", value: "MEDITERRANEAN" },
    { label: "Farmhouse", value: "FARMHOUSE" },
    { label: "Victorian", value: "VICTORIAN" },
    { label: "Gothic", value: "GOTHIC" },
    { label: "Moroccan", value: "MOROCCAN" },
    { label: "Southwestern", value: "SOUTHWESTERN" },
    { label: "Transitional", value: "TRANSITIONAL" },
    { label: "Maximalist", value: "MAXIMALIST" },
    { label: "Arabic", value: "ARABIC" },
    { label: "Japandi", value: "JAPANDI" }
];

})

$w('#generateDesignButton').onClick(async () => {
  const requestId = v4uuid();
  const channel = { name: `virtualStaging_${requestId}` };
  let isCompleted = false;
  let progressInterval;

  try {
    // Disable the button and show progress indicator
    $w('#generateDesignButton').disable();
    $w('#progressIndicator').value = 0;
    $w('#progressIndicator').show();

    const inputImageUrl = $w('#input-image-preview').src;
    const roomType = $w('#roomTypeDropdown').value;
    const designStyle = $w('#designStyleDropdown').value;
    const numImages = 1;

    // Start progress animation
    startProgressAnimation();

    // Subscribe to realtime updates
    wixRealtime.subscribe(channel, (message) => {
      const { status, result, error } = message.payload;
      
      if (status === 'completed' && !isCompleted) {
        isCompleted = true;
        handleResult(result, designStyle, roomType);
        completeProcess();
      } else if (status === 'error') {
        console.error('Error:', error);
        completeProcess(error);
      }
    });

    // Start the virtual staging process, and wait on the channel for response.
    try {
      await startVirtualStaging(requestId, inputImageUrl, roomType, designStyle, numImages);
    } catch (error) {
		; // Ignore this error, which is mostly likely a timeout 504 error cuased by hard deadline enforced by WIX.
    }

    // Set up a timeout. if we don't receive a response on the channel in 2 minutes we declare it as an error. We expect job to be completed under 2 minutes.
    setTimeout(() => {
      if (!isCompleted) {
        console.log("Request timed out. Please try again.");
        completeProcess("Request timed out. Please try again.");
      }
    }, 120000); // 120 seconds timeout

  } catch (error) {
    console.error('Error:', error);
    completeProcess(error);
  }

  function startProgressAnimation() {
    const totalTime = 30000; // 30 seconds
    const intervalTime = 100; // Update every 100ms
    const steps = totalTime / intervalTime;
    let currentStep = 0;

    progressInterval = setInterval(() => {
      currentStep++;
      let progress = (currentStep / steps) * 100;
      if (progress > 95) progress = 95;
      $w('#progressIndicator').value = progress;

      if (currentStep >= steps) {
        clearInterval(progressInterval);
      }
    }, intervalTime);
  }

  function completeProcess(error = null) {
    clearInterval(progressInterval);
    $w('#progressIndicator').value = 100;
    setTimeout(() => {
      $w('#generateDesignButton').enable();
      $w('#progressIndicator').hide();
	  $w('#progressIndicator').value = 0; // Ready for next  session
      
      if (error) {
        // Show error message to user
        $w('#errorMessage').text = typeof error === 'string' ? error : "An error occurred. Please try again.";
        $w('#errorMessage').show();
      } else {
        $w('#errorMessage').hide();
      }
    }, 500); // Short delay to show 100% completion

	
  }
});


function handleResult(result, designStyle, roomType) {
  if (result.info && result.info.images && result.info.images.length > 0) {
    const generatedImageUrl = result.info.images[0].url;
    $w('#outputImage').src = generatedImageUrl;
  }
}


let uploadedImageUrl;

$w('#uploadButton').onChange(() => {
  $w('#uploadStatusText').text = "File selected. Click upload to proceed.";
});

$w('#uploadTriggerButton').onClick(() => {
  if ($w("#uploadButton").value.length > 0) {
    $w('#uploadStatusText').text = "Uploading...";
    
    $w("#uploadButton").startUpload()
      .then((uploadedFile) => {
        uploadedImageUrl = uploadedFile.url;
        $w('#uploadStatusText').text = "Upload successful";
        // You can now use uploadedImageUrl in your API call or other functions
		$w("#input-image-preview").src = convertWixImageUrl (uploadedImageUrl);
		console.log ("Uploaded file url : " + convertWixImageUrl (uploadedImageUrl));
      })
      .catch((error) => {
        $w('#uploadStatusText').text = "Upload failed";
        console.error("Upload error:", error);
      });
  } else {
    $w('#uploadStatusText').text = "Please choose a file to upload";
  }
});


function convertWixImageUrl(wixImageUrl) {
  if (wixImageUrl.startsWith('wix:image://v1/')) {
    let convertedUrl = wixImageUrl.replace('wix:image://v1/', 'https://static.wixstatic.com/media/');
    const match = convertedUrl.match(/\/([^/]+)$/);
    if (match && match[1]) {
      convertedUrl = convertedUrl.replace(match[0], '');
    }
    return convertedUrl;
  } else {
    return wixImageUrl;
  }
}


$w('#outputImage').onClick((event) => {
  console.log ("image is clicked") 
  $w("#downloadIcon").link = $w('#outputImage').src
})