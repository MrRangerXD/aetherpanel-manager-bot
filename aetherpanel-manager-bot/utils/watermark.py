# AetherPanel Manager Bot
# Made by ZenseiBabe

try:
    import discord
except ImportError:
    pass

WATERMARK_TEXT = "Made by ZenseiBabe • AetherPanel Manager"

def apply_watermark(embed_dict: dict) -> dict:
    """
    Applies the ZenseiBabe watermark to an embed dictionary payload.
    """
    if not embed_dict:
        embed_dict = {}
    footer_text = WATERMARK_TEXT
    if "footer" in embed_dict and isinstance(embed_dict["footer"], dict):
        orig_text = embed_dict["footer"].get("text", "")
        if orig_text and orig_text != WATERMARK_TEXT and "Made by ZenseiBabe" not in orig_text:
            footer_text = f"{orig_text} | {WATERMARK_TEXT}"
    embed_dict["footer"] = {"text": footer_text}
    return embed_dict

def apply_watermark_to_discord_embed(embed) -> None:
    """
    Mutates a discord.Embed to add the required watermark footer.
    """
    if not embed:
        return
    footer_text = WATERMARK_TEXT
    if embed.footer and embed.footer.text:
        orig_text = embed.footer.text
        if orig_text and orig_text != WATERMARK_TEXT and "Made by ZenseiBabe" not in orig_text:
            footer_text = f"{orig_text} | {WATERMARK_TEXT}"
    embed.set_footer(text=footer_text)
