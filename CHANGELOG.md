# Changelog

All notable changes to this project will be documented in this file.

## [3.0.0] - 2025-07-03

### Added
- **Default Browser Detection**: Automatic detection of user's default browser across all platforms
- **Extended Browser Support**: Added support for Brave Browser, Opera, and Opera GX
- **Smart Browser Prioritization**: Default browser gets highest priority and visual indicators
- **Intelligent Browser Sorting**: Browsers sorted by preference (default first, then by compatibility)
- **Visual Browser Indicators**: Default browser marked with 🌟 and special colors
- **Cross-Platform Default Detection**: Windows (Registry), macOS (LaunchServices), Linux (xdg-settings)
- **Enhanced Browser Manager**: Comprehensive browser detection and management system

### Changed
- **Login UI Enhancement**: Dynamic browser selection with priority-based ordering
- **Browser Recommendation**: Now prioritizes user's default browser over system defaults
- **Documentation Updates**: Updated all documentation to reflect new browser support
- **Test Suite Enhancement**: Improved testing with default browser detection verification

### Fixed
- **Browser Availability**: Better detection of browser installation and availability
- **Cookie Extraction**: Improved error handling for browser-specific cookie extraction
- **UI Responsiveness**: Better handling of single vs. multiple browser scenarios

### Technical Details
- Added `_get_default_browser()` methods for all platforms
- Extended `supported_browsers` dictionary with priority system
- Implemented `get_available_browsers_sorted()` for smart ordering
- Enhanced `get_browser_recommendation()` with default browser priority
- Added support for Brave, Opera, and Opera GX cookie extraction

## [2.0.0] - 2025-07-03

### Added
- **Multi-browser support**: Added support for Chrome, Firefox, Edge, and Safari browsers
- **Browser detection**: Automatic detection of available browsers on the system
- **Browser manager module**: New `browser_manager.py` module to handle browser operations
- **Dynamic UI updates**: Login window now dynamically shows available browsers
- **Improved error handling**: Better error messages for browser-specific issues
- **Browser selection**: Users can now choose from multiple available browsers for cookie login

### Changed
- **Login window**: Updated to show available browsers instead of Chrome-only option
- **Cookie loading**: Refactored to use new browser manager for multi-browser support
- **Documentation**: Updated README files to reflect multi-browser support
- **User messages**: Updated status messages to show specific browser names

### Fixed
- **Browser compatibility**: Fixed issue where only Chrome was supported
- **Error messages**: More descriptive error messages for browser-specific failures
- **UI responsiveness**: Better handling of cases where no browsers are available

### Technical Details
- Added `BrowserManager` class to handle browser detection and cookie extraction
- Modified `UdemyEnroller.load_cookies_from_browser()` to accept browser ID parameter
- Updated `LoginWindow` to dynamically create browser selection UI
- Maintained backward compatibility with existing `load_cookies_from_chrome()` method

## [1.0.0] - 2025-07-02

### Added
- Initial release with basic functionality
- Chrome browser support for cookie authentication
- Email/password login support
- Modern GUI with dark/light theme support
- Course discovery and enrollment features
- Smart filtering and scheduling
- Comprehensive documentation in English and Arabic

### Features
- Multi-source course scraping
- Automated enrollment system
- Advanced filtering options
- Desktop notifications
- Debug mode for troubleshooting
- Export functionality for course data
