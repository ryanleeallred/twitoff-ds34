from .models import User
import numpy as np
from sklearn.linear_model import LogisticRegression
from .twitter import vectorize_tweet


def predict_user(user0_username, user1_username, hypo_tweet_text):

    # Query for the two users from the DB
    user0 = User.query.filter(User.username == user0_username).one()
    user1 = User.query.filter(User.username == user1_username).one()

    # Get the word embeddings from the user's tweets
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # Combine their vectorizations into a big X matrix
    X = np.vstack([user0_vects, user1_vects])

    # Create some 0s and 1s to generate a y vector
    # #(0s at the top (first), 1s at the bottom (second))
    y = np.concatenate([np.zeros(len(user0.tweets)),
                       np.ones(len(user1.tweets))])

    # Train our logistic regression
    log_reg = LogisticRegression()
    log_reg.fit(X, y)

    # get the word embedding for our hypothetical tweet
    # make sure the word embedding is 2D
    hypo_tweet_vect = np.array([vectorize_tweet(hypo_tweet_text)])

    # Generate a prediction
    prediction = log_reg.predict(hypo_tweet_vect)

    # return just the integer value from inside of the prediction array
    return prediction[0]
