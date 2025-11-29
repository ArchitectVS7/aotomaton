"""Conditional routing functions for workflow transitions."""

from typing import Literal
import os
import logging

from .state import ThursianState

logger = logging.getLogger(__name__)


def route_after_execution(
    state: ThursianState
) -> Literal["execution_node", "validation_node"]:
    """
    Route after execution - check if output file exists and is complete.

    Returns:
        "execution_node" - Loop back, keep waiting for completion
        "validation_node" - Proceed to validation
    """
    output_file = state.get('output_file_path')

    if not output_file or not os.path.exists(output_file):
        logger.debug("Output file not found, looping back to execution")
        return "execution_node"  # Loop back - keep waiting

    # Check if file contains completion marker
    try:
        with open(output_file, 'r') as f:
            content = f.read()

        if "Status: COMPLETE" in content or "Status:** COMPLETE" in content:
            logger.info("Execution complete, proceeding to validation")
            return "validation_node"  # Proceed

        logger.debug("Output file exists but not marked complete, looping back")
        return "execution_node"  # Loop back

    except Exception as e:
        logger.error(f"Error reading output file: {e}")
        return "execution_node"  # Loop back on error


def route_after_validation(
    state: ThursianState
) -> Literal["validation_node", "completion", "execution_node"]:
    """
    Route after validation - check validation result.

    Returns:
        "validation_node" - Loop back, keep waiting for validation
        "completion" - Validation approved, proceed to completion
        "execution_node" - Needs revision, return to execution
    """
    validation_file = state.get('validation_file_path')

    if not validation_file or not os.path.exists(validation_file):
        logger.debug("Validation file not found, looping back to validation")
        return "validation_node"  # Loop back

    # Check validation status
    try:
        with open(validation_file, 'r') as f:
            content = f.read()

        if "Status: APPROVED" in content or "Status:** APPROVED" in content:
            logger.info("Validation approved, proceeding to completion")
            return "completion"  # Approved

        if "Status: NEEDS_REVISION" in content or "Status:** NEEDS_REVISION" in content:
            logger.info("Validation requires revision, returning to execution")
            return "execution_node"  # Rework needed

        logger.debug("Validation file exists but status unclear, looping back")
        return "validation_node"  # Loop back

    except Exception as e:
        logger.error(f"Error reading validation file: {e}")
        return "validation_node"  # Loop back on error
