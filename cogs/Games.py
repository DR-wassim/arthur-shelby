import discord
from discord.ext import commands
import random 
from random import choice

nicknames = [ 'Accidental Genius', 'Ace', 'Adorable', 'Alpha', 'Amazing', 'Angel Eyes', 'Angel Face', 'Angel Heart', 'Angelito', 'Atom', 'Autumn', 'Azúcar', 'Baba Ganoush', 'Bad Kitty', 'Bam Bam', 'Bambi', 'Beagle', 'Bean', 'Beanie', 'Bear', 'Bearded Genius', 'Biggie', 'Biscuit', 'Bitsy', 'Blister', 'Blondie', 'Blue Eyes', 'Blueberry', 'Book Worm', 'Boss', 'Bowie', 'Bowler', 'Brainiac', 'Brave Heart', 'Breadmaker', 'Bright Eyes', 'Bro', 'Brown Eyes', 'Buckeye', 'Buckshot', 'Buddy', 'Bugger', 'Buster', 'Butcher', 'Button', 'Cabbie', 'Cadillac', 'Cakes', 'Candy', 'Captain', 'Captain Peroxide', 'Caramel', 'Care Bear', 'Caretaker', 'Champ', 'Chardonnay', 'Charming', 'Chef', 'Chicago Blackout', 'Chocolate Thunder', 'Chubs', 'Chuckles', 'Cinnamon', 'Claws', 'Coco', 'Commando', 'Confessor', 'Cookie', 'Cool Whip', 'Cosmo', 'Crash Override', 'Crash Test', 'Crazy Eights', 'Cream', 'Cuddle Bear', 'Cuddle Buddy', 'Cuddle Bug', 'Cuddle Bunny', 'Cuddle Muffin', 'Cuddly Bear', 'Cuddly Wuddly', 'Cupcakes', 'Curls', 'Cute Bunny', 'Cute Pie', 'Cuteness', 'Cutesy Pie', 'Cutie', 'Cutie Boo', 'Cutie Head', 'Cutie Pants', 'Cutie Patootie', 'Cutie Pie', 'Daddy', 'Dancing Madman', 'Dark Horse', 'Darling', 'Dashing', 'Dear', 'Dear Heart', 'Dearest', 'Dearest One', 'Dearie', 'Deep Water', 'Destiny', 'Dew Drop', 'Diamond', 'Dimples', 'Dolce', 'Dove', 'Dragonfly', 'Dream Boat', 'Dream Guy', 'Dream Lover', 'Dreamer', 'Dreamweaver', 'Dreamy', 'Duckling', 'Eclipse', 'Egghead', 'Electric Player', 'Elf', 'Enigma', 'Everything', 'Eye Candy', 'Fantasy', 'Favorite', 'Feisty', 'Fine Wine', 'Firecracker', 'Firefly', 'Flakes', 'Flame', 'Flash', 'Flint', 'Fluffy', 'Foxy', 'Freak', 'Freckles', 'Frostbite', 'Frozen Fire', 'Fruit Cake', 'Fruit Loop', 'Fun Size', 'Gangsta', 'Gas Man', 'Gem', 'Genie', 'Genius', 'Ghost', 'Giggles', 'Gold', 'Good Looking', 'Goody Goody', 'Goof', 'Goof Ball', 'Goofy', 'Google', 'Gorgeous', 'Grasshopper', 'Grave Digger', 'Green', 'Grimm', 'Guillotine', 'Gumdrop', 'Gummy Bear', 'Gunhawk', 'Happiness', 'Happy Face', 'Haven', 'Heart & Soul', 'Heart Stopper', 'Heart Throb', 'Heart’s Desire', 'Heartbreaker', 'Heartie', 'Heaven Sent', 'Hero', 'Hightower', 'Hobbit', 'Hog Butcher', 'Hollywood', 'Honey', 'Honey Bagel', 'Honey Bear', 'Honey Bee', 'Honey Bird', 'Honey Bun', 'Honey Bunch', 'Honey Bunny', 'Honey Lips', 'Honey Love', 'Honey Muffin', 'Honey Pie', 'Honey Pot', 'Honey Sugar Bumps', 'Honeysuckle', 'Hop', 'Hot Cakes', 'Hot Chocolate', 'Hot Lips', 'Hot Pants', 'Hot Stuff', 'Hotness', 'Hotshot', 'Hotsy-Totsy', 'Hottie', 'Hottie Tottie', 'Houston', 'Hubba Bubba', 'Huggie', 'Huggies', 'Huggy Bear', 'Hugster', 'Hun', 'Hyper', 'Ivy', 'Jazzy', 'Jester', 'Jewel', 'Jigsaw', 'Jockey', 'Joker’s Grin', 'Joy', 'Judge', 'K-9', 'Keystone', 'Khal', 'Kickstart', 'Kiddo', 'Kill Switch', 'Kingfisher', 'Kissy Face', 'Kit Kat', 'Kitchen', 'Kitten', 'Kitty Cat', 'Knockout', 'Knuckles', 'Lady Killer', 'Lamb', 'Lamb Chop', 'Lambkin', 'Lambkins', 'Lapooheart', 'Legs', 'Lemon', 'Life Mate', 'Lifeline', 'Light Priest', 'Lightning Ball', 'Lil Dove', 'Lil One', 'Lil’ Heart Breaker', 'Liquid Science', 'Little Bear', 'Little Bit', 'Little Bits', 'Little Cobra', 'Little Dove', 'Little General', 'Little Guy', 'Little Lamb', 'Little Puff', 'Lollipop', 'Looker', 'Lord Nikon', 'Lovatar', 'Love', 'Love Bear', 'Love Boodle', 'Love Bug', 'Love Face', 'Love Genie', 'Love Lumps', 'Love Muffin', 'Love Nugget', 'Lovebird', 'Lover Boy', 'Lover Doll', 'Lucky', 'Lucky Charm', 'Luna', 'Lunar', 'Mad Jack', 'Magic', 'Magic Guy', 'Magician', 'Major', 'Manimal', 'Marbles', 'Married Man', 'Marshmallow', 'Mellow', 'Melody', 'Mental', 'Micro', 'Mine', 'Mini', 'Mini Me', 'Minion', 'Minnie Mouse', 'Misty Eyes', 'Mon Amour', 'Mon Coeur', 'Monkey', 'Mookie', 'Mooky Porky', 'Moon Beam', 'Moonlight', 'Moonshine', 'Motherboard', 'Mouse', 'Movie Star', 'Fabulous', 'Gadget', 'Lucky', 'Peppermint', 'Spy', 'Thanksgiving', 'Wholesome', 'Muffin', 'Munchies', 'Munchkin', 'Nacho', 'Natural Mess', 'Nibbles', 'Night Train', 'Nightmare King', 'Nine', 'Ninja', 'Nugget', 'Num Nums', 'Nutty', 'Odd Duck', 'Omega', 'One and Only', 'Onion King', 'Oreo', 'Other Half', 'Overrun', 'Pancake', 'Panda', 'Panda Bear', 'Papa Smurf', 'Paradise', 'Paramour', 'Passion', 'Passion Fruit', 'Peach', 'Peaches', 'Peaches and Crème', 'Peachy', 'Peachy Pie', 'Peanut', 'Pearl', 'Pebbles', 'Perfect', 'Pet', 'Pickle', 'Pickle Pie', 'Pikachu', 'Pineapple', 'Pineapple Chunk', 'Pint Size', 'Pipsqueak', 'Pluto', 'Poker Face', 'Pop Tart', 'Precious', 'Prince', 'Prize', 'Prometheus', 'Psycho Thinker', 'Pudding', 'Pumpkin', 'Pumpkin Pie', 'Punk', 'Puppy', 'Pusher', 'Quake', 'Quirky', 'Rabbit', 'Radical', 'Raindrop', 'Rashes', 'Ray', 'Rebel', 'Red', 'Ride or Die', 'Roadblock', 'Rockstar', 'Rooster', 'Rug-Rat', 'Rum-Rum', 'Runner', 'Saint', 'Sandbox', 'Santa Baby', 'Scooter', 'Scrapper', 'Screwtape', 'Scrumptious', 'Serial Killer', 'Sex Bomb', 'Sex Kitten', 'Sex Muffin', 'Sexiness', 'Sexual Chocolate', 'Sexy', 'Sexy Angel', 'Sexy Bear', 'Sexy Devil', 'Sexy Dork', 'Sexy Eyes', 'Sexy Guy', 'Sexy Pants', 'Sexy Pie', 'Shadow', 'Shadow Chaser', 'Share Bear', 'Sherwood Gladiator', 'Shining Star', 'Shooter', 'Short Stuff', 'Shortcake', 'Shorty', 'Shot Glass', 'Shrimpy', 'Shug', 'Shy', 'Sidewalk Enforcer', 'Silly Goose', 'Skippy', 'Skittles', 'Skull Crusher', 'Sky', 'Sky Bully', 'Slick', 'Slicky', 'Slow Trot', 'Small Fry', 'Smallie', 'Smart Cookie', 'Smarty', 'Smiles', 'Smiley', 'Smiley Face', 'Snake Eyes', 'Snappy', 'Snicker Doodle', 'Snookums', 'Snow Bunny', 'Snow Hound', 'Snow Pea', 'Snowflake', 'Snuggle Able', 'Snuggle Bear', 'Snuggles', 'Snuka Bear', 'Soda Pop', 'Sofa King', 'Soldier', 'Soul Friend', 'Soul Mate', 'Spark', 'Sparky', 'Speedwell', 'Sphinx', 'Spiky', 'Spirit', 'Sport', 'Spring', 'Springheel Jack', 'Sprinkles', 'Squatch', 'Squirrel', 'Squishy', 'Stacker of Wheat', 'Star', 'Star Bright', 'Star Light', 'Stepper', 'Sugams', 'Sugar', 'Sugar Babe', 'Sugar Bear', 'Sugar Biscuit', 'Sugar Boy', 'Sugar Lips', 'Sugar Man', 'Sugar Pants', 'Suicide Jockey', 'Suitor', 'Sunflower', 'Sunshine', 'Super Guy', 'Super Man', 'Super Star', 'Swampmasher', 'Sweet', 'Sweet Baby', 'Sweet Dream', 'Sweet Heart', 'Sweet Kitten', 'Sweet Lips', 'Sweet Love', 'Sweet Lover', 'Sweet One', 'Sweet Tart', 'Sweet Thang', 'Sweetie', 'Swerve', 'Tacklebox', 'Take Away', 'Tarzan', 'Tater Tot', 'Tea Cup', 'Teddy', 'Teddy Bear', 'Tender Heart', 'Tesoro', 'The China Wall', 'Thrasher', 'Tiger', 'Tiggy', 'Tiny Boo', 'Toe', 'Toolmaker', 'Tough Guy', 'Tough Nut', 'Treasure', 'Treasure Trove', 'Tricky', 'Trip', 'True Love', 'TumTums', 'Turtle', 'Turtle Dove', 'Tweetie', 'Tweetie-Pie', 'Tweetums', 'Twinkie', 'Twinkle Toes', 'Twitch', 'Uber', 'Ultimate', 'Unicorn', 'Unstoppable', 'Untamed', 'Vagabond Warrior', 'Valentine', 'Viking', 'Vita', 'Voluntary', 'Vortex', 'Waffles', 'Washer', 'Waylay Dave', 'Wee-One', 'Westie', 'Wheels', 'Wolfie', 'Wonder Guy', 'Wonder Man', 'Wonderful', 'Woo Bear', 'Woo Woo', 'Woody', 'Wookie', 'Wookums', 'Wordsmith', 'Wuggle Bear', 'Wuggles', 'Xoxo', 'Yankee', 'Young Guy', 'Youngest', 'Yummers', 'Yummy', 'Yummy Bear', 'Zany', 'Zesty Dragon', 'Zod', 'Abba Zabba', 'Almond Joy', 'Amorcita', 'Angel', 'Angel Baby', 'Angel Face', 'Angel Legs', 'Angel Wing', 'Angelita', 'Aphrodite', 'Babe', 'Baby', 'Baby Bear', 'Baby Carrot', 'Baby Doll', 'Baby Girl', 'Baby Love', 'Baby Spice', 'Babycakes', 'Bambi', 'Barbie', 'Bean', 'Bear', 'Beautiful', 'Beauty', 'Bella', 'Betty Boo', 'Big Love', 'Bite-size', 'Bitty Love', 'Blondie', 'Blueberry Pie', 'Bonita', 'Boo', 'Booboo', 'Bookworm', 'Booty Beauty', 'Bossy', 'Brownie', 'Bubba', 'Bubble Butt', 'Bubble Gum', 'Bubbles', 'Buddy', 'Bug', 'Bugaboo', 'Bugaloo', 'Buggly Boo', 'Bundt Cake', 'Butter Butt', 'Butter Tart', 'Butterbomb', 'Butterbutt', 'Buttercup', 'Butterfinger', 'Butterfly', 'Butterscotch', 'Button', 'Candy Cane', 'Carmel', 'Carmelita', 'Carmella', 'Cat woman', 'Cheezit', 'Cherubie', 'Chicken Tender', 'Chicken Wing', 'Chiquitita', 'Chubby Cheeks', 'Chubs', 'Cinderella', 'Cinnabon', 'Cinnamon', 'Cookie', 'Corn Nut', 'Cowgirl', 'Cracker Jack', 'Crispie Treat', 'Critter', 'Cuddle Bug', 'Cuddly Boop', 'Cuddly Duddly', 'Cupcake', 'Curls', 'Curly-Q', 'Curvy', 'Cute Boot', 'Cute Bot', 'Cuteness', 'Cutie', 'Cutie Bug', 'Cutie Buggles', 'Cutie Cuddles', 'Cutie Patootie', 'Cutie Pie', 'Cutie Sniggles', 'Cutie Snuggles', 'Cutie Toes', 'Cutie Wiggles', 'Daisy', 'Damsel', 'Darling', 'Dear', 'Dearest', 'Dibbles', 'Dilly Dolly', 'Dimples', 'Doll face', 'Dolly', 'Dorito', 'Double Bubble', 'Double Love', 'Double Stuff', 'Double Trouble', 'Dove', 'Dovey Lovey', 'Dream Girl', 'Duchess', 'Dum Dum', 'Dumpling', 'Ella', 'Enchantress', 'Fibbles', 'Fillity Tuna', 'Filly Billy', 'Flame', 'Foxy Lady', 'French Fry', 'Frito', 'Funfetti', 'Funion', 'Fun-size', 'Gaga', 'Gibbles', 'Giggles', 'Glass of Sunshine', 'Goal Baby', 'Goddess', 'Goldie', 'Goldie Locks', 'Goo Goo', 'Goober', 'Goody Bar', 'Gorgeous', 'Green Love', 'Gribbles', 'Gubble Bum', 'Gumball', 'Gumdrop', 'Gummy Bear', 'Gummy Worm', 'Half Pint', 'Heaven-Sent', 'Hershey’s', 'Honey', 'Honey Buns', 'Honey Butt', 'Honey Loaf', 'Honey Tots', 'Honey Wiggles', 'Honeymaid', 'Honeypot', 'Hot Bod', 'Hot Butt', 'Hot Cakes', 'Hot Cross Buns', 'Hot French Fry', 'Hot Mama', 'Hot Potato', 'Hot Sauce', 'Hot Tater Tot', 'Hot Thing', 'Hotlips', 'Hottie Po-tottie', 'Hurricane', 'Icee Pop', 'Ittle Skittle', 'Itty Bitty Sugar Bomb', 'Jammer', 'Jazzie', 'Jellie Belly', 'Jelly Bean', 'Jelly Belly', 'Jelly Sweets', 'Jellybean', 'Jolly Rancher', 'Juicy', 'Juicy Fruity', 'Juliet', 'Junior Mint', 'Khaki Lassie', 'Kiddo', 'Kit Kat', 'Kitten', 'Kitty', 'Lady Bug', 'Lady Godiva', 'Laffy Taffy', 'Lervey Dervy', 'Libbles', 'Lifesaver', 'Lil Antoinette', 'Lil Ma’am', 'Lil Mama', 'Lil Miss', 'Lioness', 'Lip Smacker', 'Little Bear', 'Little Love', 'Little Mama', 'Little Rascal', 'Loca', 'Lolita', 'Lolli Lolli', 'Lollipop', 'Love', 'Love Bud', 'Love Muffin', 'Love on Fire', 'Lovebug', 'Lover Girl', 'Lovey', 'Lovey Butt', 'Lovey Dovey', 'Lovey Tickles', 'Luvski', 'Luvvy Wuvvy', 'M&M', 'Mallow Cup', 'Mama of Drama', 'Mamacita', 'Mami', 'Maple Leaf', 'Marshymallow', 'Meow', 'Mi Novia-citita', 'Milk Dud', 'Milly', 'Mine', 'Minnie', 'Missy', 'Misty May', 'Momacita', 'Monkey', 'Monkey Toes', 'Mooncake', 'Mouse', 'Muffin', 'Muffin Butt', 'Munchkin', 'My Darling', 'My Love', 'My Lovely', 'My Sunshine', 'Names Inspired by Angels', 'Nibbles', 'Nutter Butter', 'Okie', 'Pancake', 'Peaches', 'Peach-o', 'Peanut', 'Pearly', 'Pearls', 'Pebbles', 'Perf Perf', 'Perky', 'Pet', 'Pickle', 'Pink Starburst', 'Pinky', 'Pippy', 'Pocket-size', 'Pookie', 'Pop Tart', 'Precious', 'Pretty', 'Pretty Lady', 'Pretty Love', 'Princesa', 'Princess', 'Princess Peach', 'Principessa', 'Principessa', 'Pudding', 'Pumpkin', 'Pumpkin Pie', 'Punk', 'Punkin', 'Pussycat', 'Quarter Note', 'Queenie', 'Raisenette', 'Rapunzel', 'Red-Hot Bon Bon', 'Rocket Pop', 'Rolo', 'Rose', 'Ruffle', 'Runt', 'Saddle', 'Sassy Lassy', 'Scarlet', 'Secret Sauce', 'Señorita', 'Sex Enchantress', 'Sex Witch', 'Sexy Lady', 'Sexy Mama', 'She’s fun, isn’t she?', 'Shortcake', 'Shorty', 'Sirena', 'Sizzle Pop', 'Skittle', 'Skittles', 'Sleeping Beauty', 'Small Fry', 'Smartie', 'Smarty Pants', 'Smiles', 'Snack', 'Snackems', 'Snibbles', 'Snickerdoodle', 'Snickers', 'Snizzle Snacks', 'Snookie', 'Snookums', 'Snow White', 'Snowflake', 'Snuggle Bug', 'Snuggle Wumps', 'Snugglebear', 'Snuggly Bear', 'Splendid', 'Sporty Spice', 'Sprout', 'Squirrel', 'Squirt', 'Steak Tip', 'Sticky Bun', 'Sugar', 'Sugar Babe', 'Sugar Bits', 'Sugar Bomb', 'Sugar Buns', 'Sugar Lips', 'Sugar Mama', 'Sugar Mouse', 'Sugar Nova', 'Sugar Plum', 'Sugar Sauce', 'Sugar Sugar', 'Sunshine', 'Supergirl', 'Sushi', 'Sweet Bun', 'Sweet Eclair', 'Sweet Heart', 'Sweet Honey Love', 'Sweet Loaf', 'Sweet Mama', 'Sweet Melody', 'Sweet Pea', 'Sweet Peach', 'Sweet Tart', 'Sweet Thing', 'Sweetie', 'Sweetie Pie', 'Sweets', 'Swiss Roll', 'Swizzle', 'Swizzly Sue Thompkins', 'Tagalong', 'Tart', 'Tastee Squeeze', 'Tater Tot', 'Teddy Graham', 'Teehee', 'Temptress', 'Thin Mint', 'Thumbelina', 'Tibbles', 'Tic Tac', 'Tiffy Taffy', 'Tigress', 'Tilly', 'Tinkerbell', 'Tiny One', 'Tippy Tappy', 'Toffee', 'Toffee Lolly', 'Tooti', 'Toots', 'Tootsie', 'Tootsie Roll', 'Tostito', 'Triple Love', 'Triscuit', 'Trolli', 'Tuggles', 'Tutta', 'Tutti Frutti', 'Tweety', 'Twinkie', 'Twinkle', 'Twix', 'Twizzle Top', 'Twizzler', 'Waffles', 'Whirly Pop', 'Whoopie Pie', 'Whopper', 'Wifey', 'Wittle Wifey', 'Wonder Girl', 'Wonder Woman', 'Wuggles', 'Yummy']
girl_nicknames = ['Ace', 'Agent', 'Alias', 'Alpha', 'Black Diamond', 'Black Lotus', 'Black Magic', 'Black Pearl', 'Black Widow', 'Blade', 'Blaze', 'Bombshell', 'Bookworm', 'Buckwild', 'Butterfly', 'Cadillac', 'Captain', 'Captain Marvel', 'Champ', 'Champagne',  'Chance', 'Chardonnay', 'Charlie’s Angel', 'Chilla', 'Claws', 'Copycat', 'Countess', 'Country bumpkin', 'Cutlass', 'Da Vinci', 'Dahlia', 'Devil', 'Diamond', 'Diva', 'Dollface', 'Dragonfly', 'Duchess', 'Dynamo', 'Eclipse', 'Empress', 'Energizer', 'Entertainer', 'Epiphany', 'Faith', 'Fight Club', 'Fighter', 'Fire Sign', 'Firefly', 'Firestarter', 'Fiery', 'First Lady', 'Flawless', 'Frostbite', 'Godzilla', 'Heat', 'Hela', 'Heroine', 'Hoops', 'Hope', 'Hottie', 'Hurricane', 'Jessica Rabbit', 'Jetta', 'Katniss', 'Knockout', 'Lady Fierce', 'Lady Luck', 'Lava', 'Lightning', 'Lioness', 'Lunar', 'Marvel', 'Mayhem', 'Mighty', 'Moonshine', 'Mother of Dragons', 'Mystery', 'Mystique', 'Mustang', 'Neptune', 'Ninja', 'Number Six', 'Onyx', 'Opaline', 'Patience', 'Queen', 'Radar', 'Rebel', 'Red Sparrow', 'Riot', 'Rookie', 'Rubble', 'Scavenger', 'Scrappy', 'Shadow', 'Sinful', 'Skyscraper', 'Slayer', 'Slim', 'Sling', 'Sparrow', 'Sphinx', 'Spike', 'Tailor Made', 'The Evil Queen', 'Thunder', 'Tick Tock', 'Tiger', 'Trinity', 'Twister', 'Venus', 'Vicious', 'Vivi', 'Warrior Princess', 'Warrior Queen', 'Warrior Woman', 'Wind', 'Wing Woman', 'Winger', 'Winter', 'Wonder Woman', 'Xena', 'Your Highness', 'Zelda']
gifs = [
    "https://i.imgur.com/YTGnx49.gif",
    "https://i.imgur.com/U37wHs9.gif",
    "https://i.imgur.com/BU2IQym.gif",
    "https://i.imgur.com/yp6kqPI.gif",
    "https://i.imgur.com/uDyehIe.gif",
    "https://i.imgur.com/vG8Vuqp.gif",
    "https://i.imgur.com/z4uCLUt.gif",
    "https://i.imgur.com/ZIRC9f0.gif",
    "https://i.imgur.com/s8m4srp.gif",
    "https://i.imgur.com/LKvNxmo.gif",
    "https://i.imgur.com/j4W4GFt.gif",
    "https://i.imgur.com/75bX4A1.gif",
    "https://i.imgur.com/dSlfpe3.gif",
    "https://i.imgur.com/JjxaT8e.gif",
    "https://i.imgur.com/QWBlOaQ.gif",
    "https://i.imgur.com/5448px6.gif",
    "https://i.imgur.com/4WJRAGw.gif",
    "https://i.imgur.com/v1sSh5r.gif"
]

failmsgs = [
    "{author} is trying to pat non-existent entity ... and failed.",
    "{author}: *pats non-existent entity*. This bad boy can accept so many pats.",
    "To be honest, I don't know what's {author} been smoking, but sorry, you can't pat non-existent entity",
    "Oh come on, is it that hard to correctly use this command?",
    "You must pat valid and existing user. Try using @ mention, username or nickname.",
    "(╯°□°）╯︵ ┻━┻"
]

patmsgs = [
    "**{user}** got a pat from **{author}**",
    "**{author}** affectionately pat **{user}**",
    "Without hesitation, **{author}** pats **{user}** with love"
]

class Games(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.name = "Games"
        self.emoji = "️:game_die:"
        self.call_name = "Games"


    @commands.command()
    @commands.cooldown(6, 60, commands.BucketType.user)
    async def pat(self, ctx, *, user: discord.Member=None):
        """Pat users."""
        author = ctx.author

        if not user:
            message = choice(failmsgs)
            await ctx.send(message.format(author=author.name))
        else:
            message = choice(patmsgs)
            pat = discord.Embed(description=message.format(user=user.name, author=author.name), color=discord.Color(0xffb6c1))
            pat.set_image(url=choice(gifs))
            await ctx.send(embed=pat)

    @commands.command(aliases = ["nickname",'nameme',"nn",'nick'],description = "[mention member] [gender optional]" , brief = "give members new nick names")
    @commands.bot_has_permissions(manage_nicknames=True)
    async def random_nick_names(self,ctx,member_info:discord.Member=None,gender = "gamer"):
        member = member_info or ctx.message.author
        name = "shitbag"
        if gender.lower() in ["girl" , "g","female","f","femme","women"]:
            name = random.choice(girl_nicknames)
        else : 
            name = random.choice(nicknames)

        try :
            await member.edit(nick=name)
        except :
            await ctx.send("your name is perfect for a dummy like you")
            return

        await ctx.send(f'{member.name} your name is ***{member.mention}*** !! deal with it !!')

    @commands.command(description = "[game code] [channel optional]",brief = "toggle mute and show code in a nice way", aliases=["aug","host"])
    async def among_us(self,ctx,code:str = None,channel : discord.VoiceChannel = None):

        leader = ctx.message.author
        if leader.is_on_mobile():
            await ctx.send(f'**unnecessary** {leader.mention} i recommend a PC user be responsible on this')

        def check_reaction(reaction,user):
            if user == leader:
                if reaction.emoji == "🔇":
                    return "mute"
                if reaction.emoji == "🔊":
                    return 'unmute'
                if reaction.emoji == "🛑":
                    return 'leave'
            return False

        embed = discord.Embed(title = "Among Us's control panel" ,colour = discord.Colour.from_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        embed.add_field(name = "Leader :" ,value=leader.name)
        embed.add_field(name= "CODE :",value=code)
        embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/945360/header.jpg?t=1581973789")
        embed.set_footer(text="you can use the 'tma' command if anything wrong happened")
        msg = await ctx.send(embed = embed)

        gameover = False

        while not gameover :
            await msg.add_reaction("🔇")
            await msg.add_reaction('🔊')
            await msg.add_reaction('🛑')

            try :
                result = await self.client.wait_for('reaction_add',timeout= 900.0, check=lambda reaction ,user: check_reaction(reaction,user))
            except :
                break

            if result[0].emoji == "🔊" :
                to_mute_members = ctx.author.voice.channel.members or channel.members
                if to_mute_members :
                    for member in to_mute_members :
                        if member.bot :
                            continue
                        if member.voice.mute :
                            await member.edit(mute = False)


            if result[0].emoji == "🔇" :
                to_mute_members = ctx.author.voice.channel.members or channel.members
                if to_mute_members :
                    for member in to_mute_members :
                        if member.bot :
                            continue
                        if not member.voice.mute :
                            await member.edit(mute = True)

            
            if result[0].emoji == "🛑" :
                gameover = True
                to_mute_members = ctx.author.voice.channel.members or channel.members
                if to_mute_members :
                    for member in to_mute_members :
                        if member.voice.mute :
                            await member.edit(mute = False)
                    

            await msg.clear_reactions()
        await msg.clear_reactions()
        await ctx.send('among us game is over')


def setup(client):
    client.add_cog(Games(client))