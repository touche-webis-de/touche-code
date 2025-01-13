// Basic Elasticsearch System
async function reply(messages) {
  const claim = messages[messages.length - 1].content; // take last message
  const topResult = (await queryElastic(claim))[0]; // get top result from Elastic
  console.log(JSON.stringify(topResult));
  return topResult.counter; // get counter to top result
}


// Simple function to query the RAD Elasticsearch server
async function queryElastic(claim, size=1, url="https://elastic-genirsim.web.webis.de/kialo/") {
  const body = JSON.stringify({
    query: {
      match: {
        claim: {
          query: claim
        }
      }
    }
  });
  const headers = new Headers();
  headers.append("Content-Type", "application/json");
  const params = { method: "POST", headers: headers, body: body };
  console.log(body);

  const response = await fetch(url + "_search?size=" + size, params);
  const responseJson = await response.json();
  if ("error" in responseJson) {
    throw new Error("Elasticsearch error: " + JSON.stringify(responseJson));
  }
  const results = responseJson.hits.hits.map((hit, index) => {
    const result = Object.assign({}, hit["_source"]);
    result.key = index + 1;
    result.id = hit["_id"];
    result.score = hit["_score"];
    return result;
  });
  return results;
}


// Simple application server -- no need to touch this code if you extend this system
import http from "http";
const server = http.createServer(async (request, response) => {
  try {
    // get request
    const requestJson = await new Promise((resolve) => {
      const bodyParts = [];
      request.on("data", (chunk) => {
          bodyParts.push(chunk);
        }).on("end", () => {
          resolve(JSON.parse(Buffer.concat(bodyParts).toString()));
        });
    });
    if (!requestJson.messages) {
      throw new Error("Missing 'messages' attribute in " + JSON.stringify(requestJson));
    }

    try {
      // generate answer
      const answer = JSON.stringify({
        message: {
          role: "assistant",
          content: await reply(requestJson.messages)
        }
      });

      // write response
      response.writeHead(200, { "Content-Type": "application/json" });
      response.write(answer);
    } catch (error) {
      console.error(error);
      response.writeHead(500);
    }
  } catch (error) {
    console.error(error);
    response.writeHead(400);
  }
  response.end()
});

const port = 8080;
server.listen(port);

