import { Permissions, webMethod } from "wix-web-module";
import { fetch } from 'wix-fetch';
import wixRealtimeBackend from 'wix-realtime-backend';
const API_KEY = "DECOR8AI_API_KEY" // Get it from https://app.decor8.ai 
const API_URL = "https://api.decor8.ai/generate_designs_for_room";


export const startVirtualStaging = webMethod(
  Permissions.Anyone,
  async (requestId, inputImageUrl, roomType, designStyle, numImages) => {
    const channel = { name: `virtualStaging_${requestId}` };
    
    try {

      wixRealtimeBackend.publish(channel, { status: 'processing' });

      const requestBody = {
        input_image_url: inputImageUrl,
        room_type: roomType,
        design_style: designStyle,
        num_images: numImages,
        scale_factor: 1,
        color_scheme: "COLOR_SCHEME_0",
        speciality_decor: "SPECIALITY_DECOR_0"
      };

      const apiResponse = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${API_KEY}`
        },
        body: JSON.stringify(requestBody)
      });

      if (!apiResponse.ok) {
        throw new Error('Failed to generate room design');
      }

      const result = await apiResponse.json();
      wixRealtimeBackend.publish(channel, { status: 'completed', result });
      return { status: 'completed', result };
    } catch (error) {
      console.error('Error generating room design:', error);
      wixRealtimeBackend.publish(channel, { status: 'error', error: error.message });
      throw error;
    }
  }
);
