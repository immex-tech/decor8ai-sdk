/**
 * TypeScript definitions for Decor8 AI SDK
 */

export interface GenerateDesignsForRoomOptions {
    inputImageUrl: string;
    roomType: string;
    designStyle: string;
    numImages?: number;
    scaleFactor?: number;
    colorScheme?: string;
    specialityDecor?: string;
    maskInfo?: string;
    prompt?: string;
    seed?: number;
    guidanceScale?: number;
    numInferenceSteps?: number;
    designStyleImageUrl?: string;
    designStyleImageStrength?: number;
    designCreativity?: number;
    webhooksData?: string;
    decorItems?: string;
}

export interface GenerateInspirationalDesignsOptions {
    roomType: string;
    designStyle: string;
    numImages?: number;
    colorScheme?: string;
    specialityDecor?: string;
    prompt?: string;
    seed?: number;
    guidanceScale?: number;
    numInferenceSteps?: number;
}

export interface GenerateDesignsOptions {
    numImages?: number;
    numCaptions?: number;
    colorScheme?: string;
    specialityDecor?: string;
    prompt?: string;
    seed?: number;
    guidanceScale?: number;
    numInferenceSteps?: number;
}

export interface RemodelOptions {
    numImages?: number;
    scaleFactor?: number;
}

export interface LandscapingOptions {
    numImages?: number;
}

export interface SketchTo3dOptions {
    numImages?: number;
    scaleFactor?: number;
    renderType?: 'perspective' | 'isometric';
}

export interface ImageInfo {
    uuid: string;
    url: string;
    width?: number;
    height?: number;
    captions?: string[];
}

export interface ApiResponse {
    error: string;
    message: string;
    info: {
        images: ImageInfo[];
        mask_info?: string;
    };
}

declare class Decor8AI {
    constructor(baseUrl?: string);

    // Virtual Staging & Design Generation
    generateDesignsForRoom(options: GenerateDesignsForRoomOptions): Promise<ApiResponse>;
    generateInspirationalDesigns(options: GenerateInspirationalDesignsOptions): Promise<ApiResponse>;
    generateDesigns(inputImage: string | Buffer, roomType: string, designStyle: string, options?: GenerateDesignsOptions): Promise<ApiResponse>;

    // Wall & Surface Modifications
    primeWallsForRoom(inputImageUrl: string): Promise<ApiResponse>;
    primeTheRoomWalls(inputImage: string | Buffer): Promise<ApiResponse>;
    changeWallColor(inputImageUrl: string, wallColorHexCode: string): Promise<ApiResponse>;
    changeKitchenCabinetsColor(inputImageUrl: string, cabinetColorHexCode: string): Promise<ApiResponse>;

    // Remodeling
    remodelKitchen(inputImageUrl: string, designStyle: string, options?: RemodelOptions): Promise<ApiResponse>;
    remodelBathroom(inputImageUrl: string, designStyle: string, options?: RemodelOptions): Promise<ApiResponse>;

    // Exterior & Landscaping
    replaceSkyBehindHouse(inputImageUrl: string, skyType: 'day' | 'dusk' | 'night'): Promise<ApiResponse>;
    generateLandscapingDesigns(inputImageUrl: string, yardType: string, gardenStyle: string, options?: LandscapingOptions): Promise<ApiResponse>;

    // Image Processing
    removeObjectsFromRoom(inputImageUrl: string, maskImageUrl?: string): Promise<ApiResponse>;
    upscaleImage(inputImage: string | Buffer, scaleFactor?: number): Promise<ApiResponse>;

    // 3D & Rendering
    sketchTo3dRender(inputImageUrl: string, designStyle: string, options?: SketchTo3dOptions): Promise<ApiResponse>;

    // Utility
    generateImageCaptions(roomType: string, designStyle: string, numCaptions?: number): Promise<ApiResponse>;
}

export = Decor8AI;
