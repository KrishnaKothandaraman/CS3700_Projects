# Project 5 Web Crawler

## Code Structure and high level approach

There are two main classes we built to complete the functions of a web crawler.

### Parser

- This class is an implementation of HTMLParser.
- This class is written is a generic manner so that behavior can be changed based on the Enum __TargetType__.
- By creating instances of this parser with a different target type, we can use one single implementation to parse HTML and retrieve
all types of data including links, CSRFTokens and flags.

### Crawler

- This class contains the main functionality associated with the web crawler.
- __send__: This method is responsible for creating a TLS socket and sending and receiving responses from the server
- __login__: This method executes the logic to perform a login and saves the tokens and sessionId from the server
- __find_flags__: This method contains the loop to keep sending requests to the server and search for links and flags using
the parser.

## Challenges faced

- The major challenge we faced was with the manual construction of HTTP requests. The login process took us a while to
understand and several tries to get right. We kept failing the login until we replicated the request made by the browser
in its entirety.
- Parsing the HTTP response was another thing that took time and testing. It took a deep understanding of HTTP to build this
parser.

## Features of good design

- The design of the parser class along with the enumeration for parser types made the implementation extremely abstract
and this helped us massively as a single line of change could produce different parsers for our different needs.
- By Randomizing which link we pop from the frontier, we did notice a big boost in performance. We guess this may be because
we do not get stuck in deep paths along a link but rather bounce around all over the website.

## Code testing

- We initially developed an asynchronous program to ensure that tests took < 200 seconds to complete instead of waiting
10 - 15 minutes. This allowed us to test new features quickly and incrementally develop the HTTP messages while testing
every time.