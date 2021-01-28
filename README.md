# Welcome To The Documentation For Intuitionistic Bot! 

Intuitionistc Bot is a twitter bot that reminds the world not to forget that there was a crisis in the foundations of mathematics that has never been adequately resolved. While classical logicians and mathematics are widely regarded as having won the debate about what theorems were true, constructive mathematicians maintain that certain of these so-called theorems are only true based on metaphysical assumptions of the mainstream mathematicians. Constructive mathematics is based on intuitionstic logic developed by Heytinhg with roots in Brouwerian mathematics. Intuitionstic logic rejects the validity of the law of excluded. This bot looks at the theorems of classical logic and tweets whether they are valid intuitionistically or not. 

It is set up to respond to tweets from @mathslogicbot


## Motivation

We have been working on a general purpose [modal logic theorem prover](http://google.co://github.com/andrewppar/ModalTheoremProver.git). We also saw that there was a bot that tweeted tautologies of classical logic. We connected the dots when we remembered that there was a connection between intuitionistic logic and the modal logic s4. We realized that we could respond to the tweets of mathslogic bot by saying whether they were also theorems of classical logic. 

## Code Style 

All of the code in this repo is pep8 compliant. 

## Features

 - Can run indefinitely listening for a tweet from a particular user
 - Can translate formulas in the language used by @mathslogic into formulas consumable by the [modal theorem prover](http://google.co://github.com/andrewppar/ModalTheoremProver.git)

## Useage

Once you have cloned the repo: 

    git clone git@github.com:andrewppar/intuitionist_bot.git

You'll have to set up a config file: 

    touch intuitionist_bot/intuitionist_bot/config.json

That contains the consumer secret, consumer key, access token, and access token secret

You'll need to set up the config. It should look something like this: 

    {
      "consumer_key":  "XXXXXXXXXXXXXXXXXXXXX", 
      "consumer_secret": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", 
      "bearer_token": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", 
      "access_token": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
      "access_token_secret": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    }

You can run the code usinng: 

    python intuitionist_bot/intuitionist_bot.py

*NOTE:* The Main file in this repo is compiled to run on Ubuntu. You can check if it runs on your system by calling: 

    ./intuitionist_bot/Main '(AtomicFormula "p")'

The result should be 
   
    CounterExample

If this doesn't happen you may have to recompile that file. Checkout the s4 branch of the modal theorem prover and follow the directions there. 

# Testing 

The tests can be run using 

	make test 
