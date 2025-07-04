from google.adk.tools import ToolContext
import google.genai.types as types
from io import BytesIO
import base64

async def _save_plot(name: str, sns_plot, tool_context: ToolContext) -> dict:
    """
    Asynchronously saves a plot object as a PNG image artifact.
    Args:
        name (str): The name to use for the saved plot file.
        plot: The plot object to be saved (should have a `savefig` method).
        tool_context (ToolContext): The context object providing the `save_artifact` method.
    Returns:
        dict: A dictionary containing the status of the operation. On success, includes the artifact version.
              On failure, includes the error message.
    """
    
    try:
        img = BytesIO()
         
        sns_plot.savefig(img, format='png', dpi=400)
        img.seek(0)

        image_artifact = types.Part(
            inline_data=types.Blob(
                mime_type="image/png",
                data=img.getvalue()
            )
        )

        base64_str = base64.b64encode(img.getvalue()).decode('utf-8')
        data_url = f"data:image/png;base64,{base64_str}"
        filename=f"{name.replace(' ', '_')}.png"

        artifact_version = await tool_context.save_artifact(
            filename=filename,
            artifact=image_artifact,
        )

        return {
            'status': 'success',
            'version': artifact_version,
            'filename': filename,
            'data_url': data_url
        }

    except Exception as e:
        return {
            'status': 'failure',
            'error': str(e)
        }
