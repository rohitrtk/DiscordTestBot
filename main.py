import discord
import os

from replit import db

# Commands
COMMAND_IDENTIFIER = '$'
COMMAND_ADD_WORD = '$aw'
COMMAND_DEL_WORD = '$dw'
COMMAND_GET_WORDS = "$gw"
COMMAND_ADD_USER = '$au'
COMMAND_DEL_USER = '$du'

# Databases
DATABASE_WORDS = 'words'
DATABASE_USERS = 'users'

class DWC_Client(discord.Client):

    """
    Called when bot comes online.
    """
    async def on_ready(self):
        print('Test bot running')

    """
    Called when a user in the discord server sends a message.
    """
    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content[0] is COMMAND_IDENTIFIER:
            await self.run_command(message)

        
        #for word in words:
        #  if word in message.content:
        #    text = '{0.author} said {1}'
        #    await message.channel.send(text.format(message, word))

    async def send_message(self, channel, message_str):
      await channel.send(message_str)

    """
    Database key "words" contains a list.
    If the database exists, update is with the new word.
    If the database does not exist, create it and add the new word.
    """
    async def add_word(self, message, word):
      channel = message.channel

      if DATABASE_WORDS in db.keys():
        # Get the database and append the new word
        words = db[DATABASE_WORDS]
        if word in words:
          await self.send_message(channel, "{0} is already in the database".format(word))
          return

        words.append(word)

        # Save the database
        db[DATABASE_WORDS] = words
        await self.send_message(channel, "Successfully added {0} to database".format(word))
      else:
        # Create a new database with the word in it
        db[DATABASE_WORDS] = [word]

    """
    Deletes a word from the "words" database.
    """
    async def delete_word(self, message, word):
      if DATABASE_WORDS not in db.keys():
        return

      channel = message.channel
      words = db[DATABASE_WORDS]
      try:
        words.remove(word)
        await self.send_message(channel, "Successfully removed {0} to database".format(word))
      except ValueError:
        await self.send_message(channel, "{0} is not in the database".format(word))

    """
    Gets all words from the "words" DATABASE_USERS
    """
    async def get_words(self, message):
      words = db[DATABASE_WORDS]
      channel = message.channel
      
      if len(words) == 0:
        await self.send_message(channel, "No words in database")
      elif len(words) == 1:
        await self.send_message(channel, '1 word found: ' + words[0])
      else:
        s = ""
        for i in range(0, len(words)):
          s += words[i]
          if i != len(words) - 1:
            s += ', '
        
        await self.send_message(channel, '{0} words found: '.format(len(words)) + s)

    """
    Database key "users" contains a list.
    If the database exists, update is with the new user.
    If the database does not exist, create it and add a new dictionary for the user.
    """
    def add_user(self, user):
        if DATABASE_USERS in db.keys():
            # Get the database and append the new user
            users = db[DATABASE_USERS]
            users.append(user)

            # Save the database
            db[DATABASE_USERS] = users
        else:
            # Create a new database with a blank dictionary
            db[DATABASE_USERS] = {}

    """
    Deletes a user from the "users" database
    """
    def delete_user(self, user):
        if DATABASE_USERS not in db.keys():
            return

        words = db[DATABASE_USERS]
        try:
            words.remove(user)
        except ValueError:
            print('{0} does not exist in the database')

    """
    Checks if the message is a command. If it is, run the appropriate command.
    Returns True if the message was a command. Returns False otherwise.
    """
    async def run_command(self, message):
        content = message.content

        content = content.split()
        """
        if len(content) < 2:
            print('Unable to process this command')
            return
        elif len(content) > 2:
            print('1 word please')
            return
        """

        command = content[0]
        if len(content) == 2:
          parameter = content[1]

        # Add word
        if command == COMMAND_ADD_WORD:
            await self.add_word(message, parameter)
            print('$aw')
        # Delete word
        elif command == COMMAND_DEL_WORD:
            await self.delete_word(message, parameter)
            print('$dw')
        # Get words
        elif command == COMMAND_GET_WORDS:
          await self.get_words(message)
          print('$gw')
        # Add user
        elif command == COMMAND_ADD_USER:
            self.add_user(parameter)
            print('$au')
        # Delete user
        elif command == COMMAND_DEL_USER:
            self.delete_user(command)
            print('$du')

client = DWC_Client()
client.run(os.environ['BOT_TOKEN'])
#client.run(os.getenv('BOT_TOKEN'))
