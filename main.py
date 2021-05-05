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
COMMAND_GET_USERS = '$gu'

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
      return
    
    await self.check_message(message)

    #for word in words:
    #  if word in message.content:
    #    text = '{0.author} said {1}'
    #    await message.channel.send(text.format(message, word))

  async def send_message(self, channel, message_str):
    await channel.send(message_str)

  """
  Checks if the user has said a tracked word
  """
  async def check_message(self, message):
    channel = message.channel
    content = message.content
    words_said = content.split()    
    
    author = str(message.author)
    users = db[DATABASE_USERS]

    if author not in users.keys():
      return

    words = db[DATABASE_WORDS]

    for word in words_said:
      if word in words:
        u = users[author]

        if word in u.keys():
          u[word] += 1
        else:
          u[word] = 1
        
        output_message = '{0} has said {1} {2} times'.format(author, word, u[word])
        await self.send_message(channel, output_message)

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
      await self.send_message(channel, "Successfully added {0} to database".format(word))

  """
  Deletes a word from the "words" database.
  """
  async def delete_word(self, message, word):
    if DATABASE_WORDS not in db.keys():
      return

    channel = message.channel

    # Get the database and attempt to remove the word. A ValueError is thrown
    # if the word is not in the database.
    words = db[DATABASE_WORDS]
    try:
      words.remove(word)
      await self.send_message(channel, "Successfully removed {0} from database".format(word))
    except ValueError:
      await self.send_message(channel, "{0} is not in the database".format(word))

  """
  Gets all words from the "words" database
  """
  async def get_words(self, message):
    words = db[DATABASE_WORDS]
    channel = message.channel
    length = len(words)

    # Message for no words in the database
    if length == 0:
      await self.send_message(channel, "No words in database")
    else:
      s = ""
      for i in range(0, len(words)):
        s += words[i]
        if i != len(words) - 1:
          s += ', '
      
      await self.send_message(channel, '{0} {1} found: '.format(length, 'word' if length == 1 else 'words') + s)

  """
  Database key "users" contains a list.
  If the database exists, update is with the new user.
  If the database does not exist, create it and add a new dictionary for the user.
  """
  async def add_user(self, message):
    # If there is no database, create a new database with a blank dictionary
    if DATABASE_USERS not in db.keys():
      db[DATABASE_USERS] = {}
    
    channel = message.channel

    # Get the database and user name
    users = db[DATABASE_USERS]
    user = message.content.split()[1]

    # Check if user is already in database
    if user in users:
      await self.send_message(channel, 'User {0} already exists in database'.format(user))
      return

    users[user] = {}
    await self.send_message(channel, 'Now tracking user {0}'.format(user))
    # Save the database
    db[DATABASE_USERS] = users
            
  """
  Deletes a user from the "users" database
  """
  async def delete_user(self, message):
    # If there is no database, don't do anything
    if DATABASE_USERS not in db.keys():
      return

    channel = message.channel

    # Get the database and user name
    users = db[DATABASE_USERS]
    user = message.content.split()[1]

    try:
      users.pop(user, None)
      await self.send_message(channel, 'Successfully removed {0} from the database'.format(user))
    except KeyError:
      await self.send_message(channel, 'User {0} does not exist in the database'.format(user))

  """
  Gets all users from the "users" database
  """
  async def get_users(self, message):
    channel = message.channel
    
    # If there is no database, don't do anything
    if DATABASE_USERS not in db.keys():
      await self.send_message(channel, 'No database found')
      return

    users = db[DATABASE_USERS]
    length = len(users)

    if length == 0:
      await self.send_message(channel, 'No users in database')
    else:
      s, i, = '', 0
      for k in users.keys():
        s += k
        if i != length - 1:
          s += ', '
        i += 1

      await self.send_message(channel, '{0} {1} found: '.format(length, 'user' if length == 1 else 'users') + s)

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
      await self.add_user(message)
      print('$au')
    # Delete user
    elif command == COMMAND_DEL_USER:
      await self.delete_user(message)
      print('$du')
    # Get users
    elif command == COMMAND_GET_USERS:
      await self.get_users(message)
      print('$gu')

intents = discord.Intents.default()
intents.members = True
client = DWC_Client(intents=intents)
client.run(os.environ['BOT_TOKEN'])
#client.run(os.getenv('BOT_TOKEN'))
