"""
YouTube Video Processor for BJJ AI Analyzer
Downloads and processes YouTube videos for analysis
"""

import yt_dlp
import os
import logging
import tempfile
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)

class YouTubeProcessor:
    def __init__(self):
        self.download_path = 'uploads'
        os.makedirs(self.download_path, exist_ok=True)
        
        # yt-dlp options
        self.ydl_opts = {
            'format': 'best[height<=720]/best',  # Max 720p to save bandwidth
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'extractaudio': False,
            'audioformat': 'mp3',
            'embed_subs': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
        }
    
    def is_valid_youtube_url(self, url):
        """Check if URL is a valid YouTube URL"""
        try:
            parsed = urlparse(url.lower())
            
            # Check for various YouTube URL formats
            valid_domains = ['youtube.com', 'www.youtube.com', 'youtu.be', 'm.youtube.com']
            
            if parsed.netloc in valid_domains:
                # For youtu.be links
                if parsed.netloc == 'youtu.be':
                    return len(parsed.path) > 1
                
                # For youtube.com links
                if 'watch' in parsed.path or 'v=' in parsed.query:
                    return True
                
                # For youtube.com/embed/ links
                if '/embed/' in parsed.path:
                    return True
            
            return False
            
        except Exception:
            return False
    
    def extract_video_id(self, url):
        """Extract YouTube video ID from URL"""
        try:
            parsed = urlparse(url)
            
            if parsed.netloc == 'youtu.be':
                return parsed.path[1:]
            
            if 'youtube.com' in parsed.netloc:
                if '/embed/' in parsed.path:
                    return parsed.path.split('/embed/')[1].split('?')[0]
                
                query_params = parse_qs(parsed.query)
                if 'v' in query_params:
                    return query_params['v'][0]
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to extract video ID from {url}: {str(e)}")
            return None
    
    def get_video_info(self, url):
        """Get video information without downloading"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    'success': True,
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'upload_date': info.get('upload_date', ''),
                    'description': info.get('description', '')[:500],  # First 500 chars
                    'thumbnail': info.get('thumbnail', ''),
                    'video_id': info.get('id', '')
                }
                
        except Exception as e:
            logger.error(f"Failed to get video info for {url}: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to get video information: {str(e)}'
            }
    
    def download_and_process(self, url):
        """Download YouTube video and prepare for analysis"""
        try:
            # Validate URL
            if not self.is_valid_youtube_url(url):
                return {
                    'success': False,
                    'message': 'Invalid YouTube URL. Please provide a valid YouTube video link.'
                }
            
            logger.info(f"🎥 Processing YouTube video: {url}")
            
            # Get video info first
            video_info = self.get_video_info(url)
            if not video_info['success']:
                return video_info
            
            # Check video duration (limit to 30 minutes for free users)
            duration = video_info.get('duration', 0)
            if duration > 1800:  # 30 minutes
                return {
                    'success': False,
                    'message': 'Video is too long (max 30 minutes). Please use a shorter video or upgrade to Pro/Black Belt.'
                }
            
            # Create safe filename
            safe_title = "".join(c for c in video_info['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:50]  # Limit length
            video_id = self.extract_video_id(url)
            filename = f"youtube_{video_id}_{safe_title}.mp4"
            filepath = os.path.join(self.download_path, filename)
            
            # Check if already downloaded
            if os.path.exists(filepath):
                logger.info(f"✅ Video already exists: {filename}")
                return {
                    'success': True,
                    'filepath': filepath,
                    'filename': filename,
                    'title': video_info['title'],
                    'duration': duration,
                    'file_size': os.path.getsize(filepath),
                    'cached': True
                }
            
            # Download video
            download_opts = self.ydl_opts.copy()
            download_opts['outtmpl'] = filepath
            
            with yt_dlp.YoutubeDL(download_opts) as ydl:
                logger.info(f"⬇️ Downloading: {video_info['title']}")
                ydl.download([url])
            
            # Verify download
            if not os.path.exists(filepath):
                return {
                    'success': False,
                    'message': 'Download failed. Please try again or check the video URL.'
                }
            
            file_size = os.path.getsize(filepath)
            logger.info(f"✅ Download complete: {filename} ({file_size} bytes)")
            
            return {
                'success': True,
                'filepath': filepath,
                'filename': filename,
                'title': video_info['title'],
                'duration': duration,
                'file_size': file_size,
                'uploader': video_info.get('uploader', 'Unknown'),
                'cached': False
            }
            
        except Exception as e:
            logger.error(f"❌ YouTube processing failed: {str(e)}")
            
            # Clean up partial downloads
            try:
                if 'filepath' in locals() and os.path.exists(filepath):
                    os.remove(filepath)
            except:
                pass
            
            # Handle specific errors
            error_message = str(e).lower()
            if 'private' in error_message or 'unavailable' in error_message:
                return {
                    'success': False,
                    'message': 'Video is private or unavailable. Please check the URL and try again.'
                }
            elif 'age' in error_message or 'restricted' in error_message:
                return {
                    'success': False,
                    'message': 'Video is age-restricted or geo-blocked. Cannot process this video.'
                }
            elif 'copyright' in error_message:
                return {
                    'success': False,
                    'message': 'Video has copyright restrictions and cannot be processed.'
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to process YouTube video: {str(e)}'
                }
    
    def cleanup_old_downloads(self, max_age_hours=24):
        """Clean up old downloaded files to save space"""
        try:
            import time
            current_time = time.time()
            cleanup_count = 0
            
            for filename in os.listdir(self.download_path):
                if filename.startswith('youtube_'):
                    filepath = os.path.join(self.download_path, filename)
                    file_age = current_time - os.path.getctime(filepath)
                    
                    # Remove files older than max_age_hours
                    if file_age > (max_age_hours * 3600):
                        try:
                            os.remove(filepath)
                            cleanup_count += 1
                            logger.info(f"🗑️ Cleaned up old file: {filename}")
                        except Exception as e:
                            logger.warning(f"Failed to remove {filename}: {str(e)}")
            
            if cleanup_count > 0:
                logger.info(f"✅ Cleanup complete: {cleanup_count} old files removed")
            
        except Exception as e:
            logger.error(f"Cleanup failed: {str(e)}")
    
    def get_video_thumbnail(self, url):
        """Get video thumbnail URL"""
        try:
            video_id = self.extract_video_id(url)
            if video_id:
                return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            return None
        except:
            return None
    
    def validate_bjj_content(self, video_info):
        """Basic validation to check if video might contain BJJ content"""
        try:
            title = video_info.get('title', '').lower()
            description = video_info.get('description', '').lower()
            
            bjj_keywords = [
                'bjj', 'jiu jitsu', 'jiu-jitsu', 'brazilian jiu jitsu',
                'grappling', 'submission', 'guard', 'mount', 'sweep',
                'armbar', 'triangle', 'choke', 'takedown', 'gi', 'no-gi',
                'wrestling', 'judo', 'mma', 'roll', 'rolling', 'sparring'
            ]
            
            content = title + ' ' + description
            
            # Check for BJJ-related keywords
            bjj_score = sum(1 for keyword in bjj_keywords if keyword in content)
            
            if bjj_score >= 2:
                return {
                    'is_bjj_related': True,
                    'confidence': min(bjj_score / 5.0, 1.0),
                    'keywords_found': [kw for kw in bjj_keywords if kw in content]
                }
            else:
                return {
                    'is_bjj_related': False,
                    'confidence': 0.0,
                    'keywords_found': []
                }
                
        except Exception as e:
            logger.error(f"BJJ content validation failed: {str(e)}")
            return {
                'is_bjj_related': True,  # Default to True if validation fails
                'confidence': 0.5,
                'keywords_found': []
            }
