import discord
from discord.ext import commands

import api
import helper
import main
import profile
import utils


class ProfileViewer(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(aliases=["pv"])
    async def profileviewer(self, ctx: commands.Context, player: str, profilename: str = None):
        creds = helper.load_json("creds", add_config_dir=False)
        api = creds["api_key"]
        skyblockapi = api.Skyblock(api)
        playerinfo = skyblockapi.get_player_profile(player)
        extraplayerinfo = skyblockapi.get_profile_skin_and_cape(skyblockapi.get_uuid(player))
        if not playerinfo["success"]:
            return

        data = ""
        for cutename in playerinfo["profiles"]:
            if profilename is None:
                if cutename["selected"]:
                    data = cutename
                continue
            if isinstance(cutename["cute_name"], str) and cutename["cute_name"].lower() == profilename.lower():
                data = cutename

        if data == "":
            await ctx.send("Invalid profile name!")

        embed = discord.Embed()
        embed.title = extraplayerinfo["name"]
        if "game_mode" in data:
            embed.title += " (" + data["game_mode"].capitalize() + ")"
        embed.title += " on " + data["cute_name"].capitalize()
        if data["selected"]:
            embed.color = discord.Color.green()
        else:
            embed.color = discord.Color.red()

        if "banking" in data:
            embed.add_field(name="Bank Balance", value=helper.format_large_number(data["banking"]["balance"]))
        # if "community_upgrades" in data:
        #     if "currently_upgrading" in data["community_upgrades"]:
        memberdata = ""
        for m, d in data["members"].items():
            if extraplayerinfo["id"] in m:
                memberdata = d
                break
        if "fairy_souls_collected" in memberdata:
            embed.add_field(name="Fairy Souls", value=memberdata["fairy_souls_collected"])

        if "pets" in memberdata:
            embed.description = "Pets (" + str(len(memberdata["pets"])) + " total)\n"
            for pet in memberdata["pets"]:
                embed.description += "Level " + str(utils.get_level(pet["exp"], pet["tier"])) + " " + pet["type"].replace("_", " ").lower().capitalize()
                if pet["heldItem"] is not None:
                    embed.description += " holding " + pet["heldItem"].replace("_", " ").lower().capitalize() + "\n"
                else:
                    embed.description += "\n"


        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ProfileViewer(bot))
