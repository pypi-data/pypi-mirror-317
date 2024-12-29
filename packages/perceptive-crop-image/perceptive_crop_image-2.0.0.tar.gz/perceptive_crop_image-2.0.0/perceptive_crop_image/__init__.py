import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("famanual_crop_cv package loaded successfully!")


from .crop import manual_crop
