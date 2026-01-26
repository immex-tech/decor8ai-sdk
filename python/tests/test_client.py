"""Unit tests for Decor8 AI SDK client.

These tests use mocking to avoid making actual API calls.
Run with: pytest test_client.py -v
"""

import pytest
from unittest.mock import patch, MagicMock
import os

# Set a dummy API key for testing
os.environ['DECOR8AI_API_KEY'] = 'test-api-key'

from decor8ai import Decor8AI
from decor8ai.constants import ROOM_TYPES, DESIGN_STYLES, SKY_TYPES, YARD_TYPES, GARDEN_STYLES


class TestDecor8AIClient:
    """Test Decor8AI client initialization."""

    def test_init_with_api_key(self):
        """Test client initialization with explicit API key."""
        client = Decor8AI(api_key="test-key")
        assert client.api_key == "test-key"
        assert client.base_url == "https://api.decor8.ai"

    def test_init_with_env_var(self):
        """Test client initialization with environment variable."""
        client = Decor8AI()
        assert client.api_key == "test-api-key"

    def test_init_with_custom_base_url(self):
        """Test client initialization with custom base URL."""
        client = Decor8AI(api_key="test-key", base_url="https://custom.api.com/")
        assert client.base_url == "https://custom.api.com"  # trailing slash stripped

    def test_init_without_api_key_raises(self):
        """Test that missing API key raises ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop('DECOR8AI_API_KEY', None)
            with pytest.raises(ValueError, match="API key required"):
                Decor8AI()


class TestGenerateDesignsForRoom:
    """Test generate_designs_for_room method."""

    @pytest.fixture
    def client(self):
        return Decor8AI(api_key="test-key")

    @pytest.fixture
    def mock_response(self):
        return {
            "error": "",
            "message": "Successfully generated designs.",
            "info": {
                "images": [
                    {"uuid": "test-uuid", "url": "https://example.com/image.jpg", "width": 768, "height": 512}
                ]
            }
        }

    @patch('decor8ai.client.requests.post')
    def test_basic_call(self, mock_post, client, mock_response):
        """Test basic generate_designs_for_room call."""
        mock_post.return_value.json.return_value = mock_response

        result = client.generate_designs_for_room(
            input_image_url="https://example.com/room.jpg",
            room_type="livingroom",
            design_style="modern",
        )

        assert result == mock_response
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args
        assert call_kwargs[1]['json']['input_image_url'] == "https://example.com/room.jpg"
        assert call_kwargs[1]['json']['room_type'] == "livingroom"
        assert call_kwargs[1]['json']['design_style'] == "modern"
        assert call_kwargs[1]['json']['num_images'] == 1

    @patch('decor8ai.client.requests.post')
    def test_with_all_optional_params(self, mock_post, client, mock_response):
        """Test with all optional parameters."""
        mock_post.return_value.json.return_value = mock_response

        result = client.generate_designs_for_room(
            input_image_url="https://example.com/room.jpg",
            room_type="bedroom",
            design_style="scandinavian",
            num_images=4,
            scale_factor=2,
            color_scheme="COLOR_SCHEME_1",
            speciality_decor="SPECIALITY_DECOR_0",
            prompt="cozy bedroom",
            seed=12345,
            guidance_scale=15.0,
            num_inference_steps=50,
            design_style_image_url="https://example.com/style.jpg",
            design_style_image_strength=0.8,
            design_creativity=0.5,
        )

        call_kwargs = mock_post.call_args
        payload = call_kwargs[1]['json']
        assert payload['num_images'] == 4
        assert payload['scale_factor'] == 2
        assert payload['design_style_image_url'] == "https://example.com/style.jpg"
        assert payload['design_creativity'] == 0.5


class TestChangeWallColor:
    """Test change_wall_color method."""

    @pytest.fixture
    def client(self):
        return Decor8AI(api_key="test-key")

    @patch('decor8ai.client.requests.post')
    def test_basic_call(self, mock_post, client):
        """Test basic wall color change."""
        mock_response = {"error": "", "info": {"images": [{"url": "https://example.com/result.jpg"}]}}
        mock_post.return_value.json.return_value = mock_response

        result = client.change_wall_color(
            input_image_url="https://example.com/room.jpg",
            wall_color_hex_code="#FF5733"
        )

        call_kwargs = mock_post.call_args
        assert "/change_wall_color" in call_kwargs[0][0]
        assert call_kwargs[1]['json']['wall_color_hex_code'] == "#FF5733"


class TestChangeKitchenCabinetsColor:
    """Test change_kitchen_cabinets_color method."""

    @pytest.fixture
    def client(self):
        return Decor8AI(api_key="test-key")

    @patch('decor8ai.client.requests.post')
    def test_basic_call(self, mock_post, client):
        """Test basic cabinet color change."""
        mock_response = {"error": "", "info": {"images": [{"url": "https://example.com/result.jpg"}]}}
        mock_post.return_value.json.return_value = mock_response

        result = client.change_kitchen_cabinets_color(
            input_image_url="https://example.com/kitchen.jpg",
            cabinet_color_hex_code="#FFFFFF"
        )

        call_kwargs = mock_post.call_args
        assert "/change_kitchen_cabinets_color" in call_kwargs[0][0]
        assert call_kwargs[1]['json']['cabinet_color_hex_code'] == "#FFFFFF"


class TestRemodelKitchen:
    """Test remodel_kitchen method."""

    @pytest.fixture
    def client(self):
        return Decor8AI(api_key="test-key")

    @patch('decor8ai.client.requests.post')
    def test_basic_call(self, mock_post, client):
        """Test basic kitchen remodel."""
        mock_response = {"error": "", "info": {"images": [{"url": "https://example.com/result.jpg"}]}}
        mock_post.return_value.json.return_value = mock_response

        result = client.remodel_kitchen(
            input_image_url="https://example.com/kitchen.jpg",
            design_style="modern"
        )

        call_kwargs = mock_post.call_args
        assert "/remodel_kitchen" in call_kwargs[0][0]
        assert call_kwargs[1]['json']['design_style'] == "modern"

    @patch('decor8ai.client.requests.post')
    def test_with_options(self, mock_post, client):
        """Test kitchen remodel with options."""
        mock_response = {"error": "", "info": {"images": []}}
        mock_post.return_value.json.return_value = mock_response

        client.remodel_kitchen(
            input_image_url="https://example.com/kitchen.jpg",
            design_style="farmhouse",
            num_images=3,
            scale_factor=2
        )

        payload = mock_post.call_args[1]['json']
        assert payload['num_images'] == 3
        assert payload['scale_factor'] == 2


class TestRemodelBathroom:
    """Test remodel_bathroom method."""

    @pytest.fixture
    def client(self):
        return Decor8AI(api_key="test-key")

    @patch('decor8ai.client.requests.post')
    def test_basic_call(self, mock_post, client):
        """Test basic bathroom remodel."""
        mock_response = {"error": "", "info": {"images": []}}
        mock_post.return_value.json.return_value = mock_response

        client.remodel_bathroom(
            input_image_url="https://example.com/bathroom.jpg",
            design_style="contemporary"
        )

        call_kwargs = mock_post.call_args
        assert "/remodel_bathroom" in call_kwargs[0][0]


class TestGenerateLandscapingDesigns:
    """Test generate_landscaping_designs method."""

    @pytest.fixture
    def client(self):
        return Decor8AI(api_key="test-key")

    @patch('decor8ai.client.requests.post')
    def test_basic_call(self, mock_post, client):
        """Test basic landscaping design."""
        mock_response = {"error": "", "info": {"images": []}}
        mock_post.return_value.json.return_value = mock_response

        client.generate_landscaping_designs(
            input_image_url="https://example.com/yard.jpg",
            yard_type="Front Yard",
            garden_style="japanese_zen"
        )

        call_kwargs = mock_post.call_args
        assert "/generate_landscaping_designs" in call_kwargs[0][0]
        payload = call_kwargs[1]['json']
        assert payload['yard_type'] == "Front Yard"
        assert payload['garden_style'] == "japanese_zen"


class TestSketchTo3DRender:
    """Test sketch_to_3d_render method."""

    @pytest.fixture
    def client(self):
        return Decor8AI(api_key="test-key")

    @patch('decor8ai.client.requests.post')
    def test_basic_call(self, mock_post, client):
        """Test basic sketch to 3D render."""
        mock_response = {"error": "", "info": {"images": []}}
        mock_post.return_value.json.return_value = mock_response

        client.sketch_to_3d_render(
            input_image_url="https://example.com/sketch.jpg",
            design_style="modern"
        )

        call_kwargs = mock_post.call_args
        assert "/sketch_to_3d_render" in call_kwargs[0][0]

    @patch('decor8ai.client.requests.post')
    def test_with_render_type(self, mock_post, client):
        """Test with render type option."""
        mock_response = {"error": "", "info": {"images": []}}
        mock_post.return_value.json.return_value = mock_response

        client.sketch_to_3d_render(
            input_image_url="https://example.com/sketch.jpg",
            design_style="modern",
            render_type="isometric"
        )

        payload = mock_post.call_args[1]['json']
        assert payload['render_type'] == "isometric"


class TestReplaceSkyBehindHouse:
    """Test replace_sky_behind_house method."""

    @pytest.fixture
    def client(self):
        return Decor8AI(api_key="test-key")

    @patch('decor8ai.client.requests.post')
    def test_basic_call(self, mock_post, client):
        """Test basic sky replacement."""
        mock_response = {"error": "", "info": {"images": []}}
        mock_post.return_value.json.return_value = mock_response

        client.replace_sky_behind_house(
            input_image_url="https://example.com/house.jpg",
            sky_type="dusk"
        )

        call_kwargs = mock_post.call_args
        assert "/replace_sky_behind_house" in call_kwargs[0][0]
        assert call_kwargs[1]['json']['sky_type'] == "dusk"


class TestRemoveObjectsFromRoom:
    """Test remove_objects_from_room method."""

    @pytest.fixture
    def client(self):
        return Decor8AI(api_key="test-key")

    @patch('decor8ai.client.requests.post')
    def test_basic_call(self, mock_post, client):
        """Test basic object removal."""
        mock_response = {"error": "", "info": {"images": []}}
        mock_post.return_value.json.return_value = mock_response

        client.remove_objects_from_room(
            input_image_url="https://example.com/room.jpg"
        )

        call_kwargs = mock_post.call_args
        assert "/remove_objects_from_room" in call_kwargs[0][0]

    @patch('decor8ai.client.requests.post')
    def test_with_mask(self, mock_post, client):
        """Test object removal with mask."""
        mock_response = {"error": "", "info": {"images": []}}
        mock_post.return_value.json.return_value = mock_response

        client.remove_objects_from_room(
            input_image_url="https://example.com/room.jpg",
            mask_image_url="https://example.com/mask.png"
        )

        payload = mock_post.call_args[1]['json']
        assert payload['mask_image_url'] == "https://example.com/mask.png"


class TestConstants:
    """Test that constants are properly defined."""

    def test_room_types(self):
        """Test room types constant."""
        assert "livingroom" in ROOM_TYPES
        assert "bedroom" in ROOM_TYPES
        assert "kitchen" in ROOM_TYPES
        assert len(ROOM_TYPES) >= 28

    def test_design_styles(self):
        """Test design styles constant."""
        assert "modern" in DESIGN_STYLES
        assert "scandinavian" in DESIGN_STYLES
        assert "minimalist" in DESIGN_STYLES
        assert len(DESIGN_STYLES) >= 42

    def test_sky_types(self):
        """Test sky types constant."""
        assert SKY_TYPES == ["day", "dusk", "night"]

    def test_yard_types(self):
        """Test yard types constant."""
        assert "Front Yard" in YARD_TYPES
        assert "Backyard" in YARD_TYPES

    def test_garden_styles(self):
        """Test garden styles constant."""
        assert "japanese_zen" in GARDEN_STYLES
        assert "mediterranean" in GARDEN_STYLES
        assert len(GARDEN_STYLES) >= 31


class TestModuleLevelFunctions:
    """Test backward-compatible module-level functions."""

    @patch('decor8ai.client.requests.post')
    def test_change_wall_color_function(self, mock_post):
        """Test module-level change_wall_color function."""
        from decor8ai import change_wall_color

        mock_response = {"error": "", "info": {"images": []}}
        mock_post.return_value.json.return_value = mock_response

        change_wall_color("https://example.com/room.jpg", "#FF0000")

        assert mock_post.called

    @patch('decor8ai.client.requests.post')
    def test_remodel_kitchen_function(self, mock_post):
        """Test module-level remodel_kitchen function."""
        from decor8ai import remodel_kitchen

        mock_response = {"error": "", "info": {"images": []}}
        mock_post.return_value.json.return_value = mock_response

        remodel_kitchen("https://example.com/kitchen.jpg", "modern")

        assert mock_post.called
