from __future__ import with_statement

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import simplejson as json
from urllib import unquote
import logging

from mg import extract_tp, read_file, generate, make_nice_text

class MainPage(webapp.RequestHandler):
    def get(self):
        """
        GET: ...
        """
        html = """
        <html>
            <body>
                <h1>Markov Chain Based Text Generator</h1>
                <p>This is a natural text generation tool. Given some 
                training text, the tool will extract a transition 
                probability matrix and use it to generate a random text.</p>
                <p>The following parameters can be used to tweak the output:</p>
                <ul>
                    <li>training text, these two text are available at the moment (send me an email if you want me to add more):
                        <ul>
                            <li><a href="http://www.gutenberg.org/ebooks/1399">Anna Karenina by Leo Tolstoy</a> 
                            <li><a href="http://www.gutenberg.org/ebooks/2591">Grimm's Fairy Tales by Jacob Grimm and Wilhelm Grimm</a>
                        </ul>
                    </li>
                    <li>percentage of words to use from learning text for generation (if this value is less than 1, only the n most common words will be used; increases computational effort)</li>
                    <li>number of output words</li>
                    <li>probability of starting a new paragraph at the end of a sentence</li>
                </ul>
                <p>Generator parameters:</p>
                <form name="generator" action="/" method="post">
                    <p>Training text: <select name="training-text">
                                        <option value="anna">Anna Karenina by Leo Tolstoy</option>
                                        <option value="grimm">Grimm's Fairy Tales by Jacob Grimm and Wilhelm Grimm</option>
                                    </select>
                    </p>
                    <p>Percenteage of input words to use for generation: <select name="num-states-factor">
                                        <option value="0.1">0.1</option>
                                        <option value="0.2">0.2</option>
                                        <option value="0.3">0.3</option>
                                        <option value="0.4" selected="selected">0.4</option>
                                        <option value="0.5">0.5</option>
                                        <option value="0.6">0.6</option>
                                        <option value="0.7">0.7</option>
                                        <option value="0.8">0.8</option>
                                        <option value="0.9">0.9</option>
                                        <option value="1.0">1.0</option>
                                    </select>
                    </p>
                    <p>Number of output words: <input type="text" name="num-words" /></p>
                    <p>Paragraph probability: 
                                    <select name="para-prob">
                                        <option value="0.1">0.1</option>
                                        <option value="0.2" selected="selected">0.2</option>
                                        <option value="0.3">0.3</option>
                                        <option value="0.4">0.4</option>
                                        <option value="0.5">0.5</option>
                                        <option value="0.6">0.6</option>
                                        <option value="0.7">0.7</option>
                                        <option value="0.8">0.8</option>
                                        <option value="0.9">0.9</option>
                                        <option value="1.0">1.0</option>
                                    </select>
                    </p>
                    <input type="submit" value="Generate" />
                </form>
            </body>
        </html>
        """

        self.response.headers["Content/Type"] = "text/html"
        self.response.out.write(html)
    
    def post(self):

        training_text = self.request.get("training-text")
        num_states_factor = float(self.request.get("num-states-factor"))
        num_words = float(self.request.get("num-words"))
        para_prob = float(self.request.get("para-prob"))s

        logging.info("Got request for [tt: %s, sf: %s, nw: %s, pp: %s]" % (training_text, num_states_factor, num_words, para_prob))

        # print "Extracting transition probabilities from learning text '%s' (this may take a long time...)" % input_file
        states, tp = extract_tp(read_file(input_file), None, num_states_factor)

        # print "Generating text (%s words)" % num_words
        text = make_nice_text(generate(states, tp, num_words, "The"), True, para_prob)
        
        html = """
        <html>
            <body>
                <p>
                    %s
                </p>
            </body>
        </html>
        """ % text

        self.response.headers["Content/Type"] = "text/html"
        self.response.out.write(html)
   

# WSGI application
application = webapp.WSGIApplication( [ (r'/', MainPage)
                                      ], debug=True
                                    )


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)


if __name__ == '__main__':
    main()

















