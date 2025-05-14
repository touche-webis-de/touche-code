# User simulation for Retrieval-Augmented Debating 2025 Sub-Task 1

To test your developed debate systems, you can use our public facing user simulation API. The examples below show how your system can interact with the API.

## Example API calls

The message formats are adaptions of the OpenAI or Ollama standard message formats. 

### Producing first user utterance
To produce the first utterance of the user, call the following endpoint and provide the claim and description of the provided data. 

**Request**
```shell
curl -X POST https://touche25-rad.webis.de/user-sim/api/chat -H "Content-Type: application/json" -d '{
  "model": "base-user",
  "options": {
    "claim": "There is nothing inherently morally wrong about lying",
    "description": "It is generally taken for granted that lying is a bad thing to do, and that it is only permissible under circumstances that \"balance it out\" in some way by having an exceptional benefit. However, I don'\''t see any reason why lying should be considered morally incorrect on its own.\nObviously, deception can be used to harm people. This is often seen now because deception is a convenient way to make someone act against their own best interest, but it is demonstrably true that it can do the reverse, or that someone can be harmfully persuaded without lying as well. Like most forms of communication, it can be used to hurt, help, or under purely neutral circumstances. This is true whether you look at it in terms of intention or consequence. There is also a possible occurrence of emotional harm, where a person feels betrayed after being lied to, but this is a feature of the current social expectation of truthfulness, not of lying itself, and it is easy to imagine situations where a person can be lied to without experiencing any emotional harm (or, inversely, where a person can be harmed by the truth).\nFor lying to be inherently morally wrong, I believe there would need to be some sort of harm which is inflicted unavoidably by every act of lying, and I can think of two possible arguments for that being the case:\nThe first argument would be if you think that each person has the moral right to complete accurate knowledge about reality, regardless of the consequences of that knowledge, and that any action which impedes that right is harmful to that individual. I don'\''t see any reason to agree with this proposition, though, and that belief itself would have some extreme and unintuitive conclusions that go against other conventional values, such as privacy.\nThe second argument would be that trust is valuable in general, and lying devalues or damages trust on one scale or another. Kant used a similar argument in an example for his own theory of the categorical imperative, where he stated that lying is logically self-contradictory because it erodes the same trust that it relies on to benefit the liar. I disagree with this in any case, though, because even if lying were fully morally acceptable there would still remain obvious benefits to telling the truth. If there is any value to trust, I think that value can just as easily be applied to skepticism, and a balance between the two.\nIf there are any other reasons I'\''m overlooking, I'\''d be interested in hearing them.\nTL;DR - Lying can harm people directly, but not in any way that is inherent to the act. It can prevent people from having a full and accurate understanding of reality, and it can generally limit the strength of trust, but I don'\''t think either of those things can be seen as necessarily morally wrong."
  }
}' 
```

**Response**
```json
{
  "model":"base-user",
  "created_at":"2025-05-14T12:57:45.920457",
  "message":{
    "role":"assistant",
    "content":"My opinion is that there is no harm that is intrinsically attached to lying itself, suggesting that honesty on moral grounds does not, in itself, mandate it."
  }
}
```

### Responding to user utterances

To respond to the provided user utterances you can use the following API requests. 

**Request**

```shell
curl -X POST https://touche25-rad.webis.de/user-sim/api/chat -H "Content-Type: application/json" -d '{
  "model": "base-user",
  "messages": [
    {"role":"assistant","content":"My opinion is that there is no harm that is intrinsically attached to lying itself, suggesting that honesty on moral grounds does not, in itself, mandate it."},
    {"role":"user","content":"I think that it is always wrong to lie since the ten commandments tell us so."}
  ]
}' 
```

**Response**

```json
{
  "model": "base-user",
  "retrieved": [
    {
      "id": "18304.404",
      "topic": "Should Google Censor Their Search Results In Order To Operate In China?",
      "tags": [
        "World",
        "Internet",
        "Technology"
      ],
      "attacks": "This understanding of morality fails to account for actions like telling a lie that will never be found out, because this causes no measurable harm. Most people intuitively demand a broader understanding of what is right or wrong.",
      "supports": "This understanding of morality succeeds in accounting for actions like telling a lie that will never be found out, because this causes no measurable harm.",
      "text": "People intuiting a certain type of morality does not necessarily mean that sense of morality is correct.",
      "references": [],
      "original": "attacks",
      "score": 0.8602762
    },
    {
      "id": "30347.508",
      "topic": "Should Evangelicals vote for Trump?",
      "tags": [
        "Religion",
        "USA",
        "Politics",
        "Trump"
      ],
      "attacks": "The Ten Commandments set out lying as a sin, and it has been found that Trump has publicly made more than 10,000 false or misleading claims.",
      "supports": "The Ten Commandments do not set out lying as a sin.",
      "text": "All presidents and presidential candidates lie and make misleading claims. Trump is not the only president who has done that.",
      "references": [
        "https://www.theamericanconservative.com/articles/our-long-history-of-presidential-lies/"
      ],
      "original": "attacks",
      "score": 0.860024
    },
    {
      "id": "32205.192",
      "topic": "Should parents perpetuate myths like Santa Claus and the Easter Bunny to their children?",
      "tags": [
        "Christmas",
        "Easter",
        "Society"
      ],
      "attacks": "From a utilitarian perspective lying to children is moral as long as the consequences of doing so are more pleasurable than they are painful.",
      "supports": "From a utilitarian perspective lying to children is not moral as long as the consequences of doing so are more pleasurable than they are painful.",
      "text": "It is difficult to predict the consequences of an action.",
      "references": [
        "http://www.bbc.co.uk/ethics/lying/lying_1.shtml"
      ],
      "original": "attacks",
      "score": 0.85295534
    },
    {
      "id": "32205.194",
      "topic": "Should parents perpetuate myths like Santa Claus and the Easter Bunny to their children?",
      "tags": [
        "Christmas",
        "Easter",
        "Society"
      ],
      "attacks": "From a utilitarian perspective lying to children is moral as long as the consequences of doing so are more pleasurable than they are painful.",
      "supports": "From a utilitarian perspective lying to children is not moral as long as the consequences of doing so are more pleasurable than they are painful.",
      "text": "It is difficult to find an appropriate unit to measure the net impact of pleasure and pain.",
      "references": [],
      "original": "attacks",
      "score": 0.85295534
    },
    {
      "id": "32205.210",
      "topic": "Should parents perpetuate myths like Santa Claus and the Easter Bunny to their children?",
      "tags": [
        "Christmas",
        "Easter",
        "Society"
      ],
      "attacks": "It is morally wrong for people to lie.",
      "supports": "It is not morally wrong for people to lie.",
      "text": "It is not so clear what virtue ethicists should do if a lie is told in pursuit of an alternative virtue. For example, it is unclear whether a lie is ethical if it is told in order to save the lives of 100 people.",
      "references": [
        "https://plato.stanford.edu/entries/ethics-virtue/"
      ],
      "original": "attacks",
      "score": 0.85258245
    },
    {
      "id": "32205.287",
      "topic": "Should parents perpetuate myths like Santa Claus and the Easter Bunny to their children?",
      "tags": [
        "Christmas",
        "Easter",
        "Society"
      ],
      "attacks": "It is morally wrong for people to lie.",
      "supports": "It is not morally wrong for people to lie.",
      "text": "Hugo Groitus argued it was morally permissible to lie to someone who has no right to the truth. For example, a mugger has no right to the truth that you have 500$ in your coat pocket.",
      "references": [
        "http://www.bbc.co.uk/ethics/lying/lying_1.shtml"
      ],
      "original": "attacks",
      "score": 0.85258245
    },
    {
      "id": "32205.612",
      "topic": "Should parents perpetuate myths like Santa Claus and the Easter Bunny to their children?",
      "tags": [
        "Christmas",
        "Easter",
        "Society"
      ],
      "attacks": "It is morally wrong for people to lie.",
      "supports": "It is not morally wrong for people to lie.",
      "text": "Lying is natural.",
      "references": [],
      "original": "attacks",
      "score": 0.85258245
    },
    {
      "id": "32205.215",
      "topic": "Should parents perpetuate myths like Santa Claus and the Easter Bunny to their children?",
      "tags": [
        "Christmas",
        "Easter",
        "Society"
      ],
      "attacks": "It is not morally wrong for people to lie.",
      "supports": "It is morally wrong for people to lie.",
      "text": "From a Kantian perspective, lying is intrinsically wrong because it robs another of the ability to make free and rational choices.",
      "references": [
        "https://www.scu.edu/ethics/ethics-resources/ethical-decision-making/lying/"
      ],
      "original": "supports",
      "score": 0.85146284
    },
    {
      "id": "32205.219",
      "topic": "Should parents perpetuate myths like Santa Claus and the Easter Bunny to their children?",
      "tags": [
        "Christmas",
        "Easter",
        "Society"
      ],
      "attacks": "From a Kantian perspective, lying is intrinsically wrong because it robs another of the ability to make free and rational choices.",
      "supports": "From a Kantian perspective, lying is not intrinsically wrong because it robs another of the ability to make free and rational choices.",
      "text": "It is not clear in all situations whether everyone possesses the ability to reason. For example, children, those with learning difficulties or those with mental health issues may not have the freedom to make rational choices.",
      "references": [],
      "original": "attacks",
      "score": 0.84854174
    },
    {
      "id": "32205.217",
      "topic": "Should parents perpetuate myths like Santa Claus and the Easter Bunny to their children?",
      "tags": [
        "Christmas",
        "Easter",
        "Society"
      ],
      "attacks": "From a Kantian perspective, lying is not intrinsically wrong because it robs another of the ability to make free and rational choices.",
      "supports": "From a Kantian perspective, lying is intrinsically wrong because it robs another of the ability to make free and rational choices.",
      "text": "A lie may lead someone to make a choice that they otherwise would not have made.",
      "references": [],
      "original": "supports",
      "score": 0.84172034
    }
  ],
  "created_at": "2025-05-14T13:05:51.079034",
  "message": {
    "role": "assistant",
    "content": "The Ten Commandments do indeed instruct us against lying, but that is a theological argument, and my stance concerns a moral evaluation, where the context and purpose of the lie come into play."
  }
}
```