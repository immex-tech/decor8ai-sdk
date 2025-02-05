# Decor8 AI SDK
Decor8 AI is a cutting-edge interior design app that revolutionizes your design experience. It offers a rich tapestry of customization options allowing you to visualize and craft interiors that echo your style and imagination. 

You can choose from 35+ interior design styles and 20+ room types to create unique interior design styles for your space.

The app specializes in virtual staging, transforming empty spaces into vivid, attractive interiors, enhancing their appeal for better marketability. 

This documentation describes how you can use Decor8 AI Python SDK to integrate Decor8 AI's powerful features in your application. In addition to Python SDK, Decor8 AI also exposes simple HTTP based API for easy integration with language of your choice.

See [complete documentation for Decor8 AI api for Virtual Staging and Interior Design](https://api-docs.decor8.ai/). Please reach out to [Decor8 AI Team](mailto:decor8@immex.tech) with questions or suggestions. 


## Table of Contents
- [What's Under the Hood?](#whats-under-the-hood)
- [Python SDK](#python-sdk)    
- [Javascript SDK](#javascript-sdk)
- [Flutter/Dart SDK](#dart-sdk)
- [HTTP/Rest API](#rest-api)

## What's Under the Hood?

This SDK provides seamless access to Decor8 AI's powerful virtual staging and interior design platform. It empowers developers with enterprise-grade interior design capabilities without requiring deep expertise in machine learning or computer vision.

While traditional Stable Diffusion and ControlNet approaches can work for basic interior design tasks, they often fall short when dealing with real-world room photos, especially for virtual staging. Decor8 AI solves this by combining:

- Advanced image segmentation to understand room layout
- Specialized Stable Diffusion models fine-tuned for interior design and virtual staging
- Enhanced ControlNet implementations for precise furniture placement
- Intelligent empty room detection and furniture filling algorithms
- Upscaler to add fine details to the generated images and improve quality

The platform handles the complex orchestration of these components, allowing developers to focus on building their applications rather than wrestling with model implementations, maintenance, and scalability. Whether you're looking to fill empty rooms with furniture or create complete interior design transformations, the API provides granular control through its parameters while ensuring consistent, production-ready results.

For developers who have experimented with various Stable Diffusion approaches for virtual staging, Decor8 AI offers a reliable, scalable alternative that just works. The platform's robust architecture ensures high availability and consistent performance, enabling rapid application development and deployment.

# <a id="python-sdk">Python SDK
[Refer to Python SDK Docs](python/decor8ai/README.md)

# <a id="javascript-sdk">Javascript SDK
[Refer to Javascript SDK Docs](js/decor8ai/README.md)

# <a id="dart-sdk">Flutter/Dart SDK
[Refer to Dart SDK Docs](dart/decor8ai/README.md)

# <a id="rest-api">Rest API
[Refer to Rest API Docs](http/README.md)

## Use Cases

### Real Estate Virtual Staging
- Transform empty properties into beautifully staged homes to attract potential buyers
- Showcase different design possibilities for the same space
- Reduce physical staging costs while maintaining visual appeal
- Perfect for real estate listings, property websites, and marketing materials

### Personal Interior Design Chatbots
- Integrate Decor8 AI into your chatbot to provide instant interior design suggestions
- Allow users to visualize room transformations through natural conversation
- Enhance customer engagement with AI-powered design recommendations
- Ideal for home improvement apps and design consultation services

### Virtual Home Staging Services
- Start your own virtual staging business with enterprise-grade AI technology
- Offer quick turnaround times with consistent, high-quality results
- Scale your business without the overhead of physical furniture inventory
- Provide multiple design options for each space at a fraction of traditional costs

### Photography Service Enhancement
- Add value to existing real estate photography services
- Differentiate your business with AI-powered staging capabilities
- Offer both traditional and virtually staged photos to clients
- Increase revenue per property with minimal additional effort

### Website & App Integration
- Seamlessly integrate virtual staging capabilities into any website or application
- Enhance user experience with real-time design visualization
- Provide interactive before/after comparisons
- Perfect for:
  - Real estate platforms
  - Interior design applications
  - Home improvement websites
  - Property management systems
  - E-commerce furniture sites

### Additional Applications
- Architectural visualization
- Interior design education
- Home renovation planning
- Furniture retail visualization
- Property development marketing

Start transforming spaces today with Decor8 AI's powerful SDK. Whether you're a developer, business owner, or service provider, our API provides the tools you need to bring professional interior design capabilities to your platform.
