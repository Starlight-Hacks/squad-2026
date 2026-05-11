## Overview

The goal of this idea is to meet three targets:

1. Distributed payment systems for informal traders with zero install.

2. Service discovery in an instant, powered by natural language processing.

3. A state-wide dashboard where institutions like the Internal Revenue Service can view trader activity, cashflow, search frequencies, heat maps, timeseries data and more.

## Distributed Payments

### Plan

We intend to use WhatsApp as our primary communication interface. A registered and authorized user may initiate payments via the automated WhatsApp messenger bot. 

All payments must be initiated from the user's registered phone number. Before any payment is completed, the user is presented with a summary of the recipient's details then prompted for their Payment Confirmation Token. 

Once valid, the backend runs its own internal fraud prevention protocols which may proceed to either reject or approve the transaction. 

Finally, the user is presented with details of the transaction and any further instructions.

### Flow

1. A user registers with their mobile phone number, full name, BVN, geo-location, and any further necessary information.

2. The API verifies that their bank details are valid and match what was provided.

3. A One Time Passcode (OTP) is sent to the user as phone number proof of ownership.

4. Once verified, the API creates a squad virtual account wallet for this user. They are directed to create a Payment Confirmation Token which is used for payment confirmation.

5. For the demo/mvp, they are also provided with the Twillio join code and phone number.

6. Payment requests are initiated on WhatsApp. The user converses in natural language such as "send 2500 naira to 8112233445 GTBank". 

7. Our models parse this intent then run sanity checks such as account balance checks, account number checks, then returns a structured response of the recipients details, prompting the user for a confirmation code. 

8. The user may also opt to back out from the transaction, in which case inactive transactions are deleted after 10 minutes.

9. Once a payment has been completed or denied, the bot responds appropriately with the transaction status.

## Service Discovery

### Plan

Service discovery is the second pillar our solution addresses. We intend to make it easy for informal traders or service workers to be discovered by potential clients. 

For instance, say you were looking for hair dressers near you. The application uses Artificial Intelligence to match against our user base of skilled workers who fit the description and are available to work in the area. In this way, our service connects workers and employers seamlessly.

### Flow

1. On the same web application, users can register as service providers. They provide personally identifiable information such as their email address, phone number, full names, geo-location, service rate etc.

2. In the future, we plan to have a verification period for any service worker.

3. On WhatsApp, a user may request for workers or traders in Natural Language such as "I'm looking for a generator repair person around Yaba".

4. Our models parse this intent, then search our worker database for description that fit this description. We intend to use vector/semantic search to enrich this experience.

5. Once successful matches are found, the API responds with likely candidates who have high credibility ratings.

6. From there onward, the user may decide to contact any of the listed profiles.

## State-wide Activity Network

> This section is in progress.
