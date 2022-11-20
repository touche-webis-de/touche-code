const fs = require("fs-extra");
const path = require('path');

const { AbstractScriptorScript, files, pages, log } = require('@webis-de/scriptor');

const NAME = "ImageSearchScript";
const VERSION = "0.1.0";

const SCRIPT_OPTION_QUERY = "query";                                       // Required. Sets the query

module.exports = class extends AbstractScriptorScript {

  constructor() {
    super(NAME, VERSION);
  }

  async run(browserContexts, scriptDirectory, inputDirectory, outputDirectory) {
    const browserContext = browserContexts[files.BROWSER_CONTEXT_DEFAULT];

    // Define script options
    const requiredScriptOptions = [ SCRIPT_OPTION_QUERY ];
    const defaultScriptOptions = {};

    // Get script options
    const scriptOptions = files.readOptions(files.getExisting(
      files.SCRIPT_OPTIONS_FILE_NAME, [ scriptDirectory, inputDirectory ]),
      defaultScriptOptions, requiredScriptOptions);
    log.info({options: scriptOptions}, "script.options");
    fs.writeJsonSync( // store options for provenance
      path.join(outputDirectory, files.SCRIPT_OPTIONS_FILE_NAME), scriptOptions);
    const query = scriptOptions[SCRIPT_OPTION_QUERY];
    const optionsSnapshot = { path: path.join(outputDirectory, "snapshot") };
    const waitEvent = "load";
    const waitNetworkMilliseconds = 5000;

    const page = await browserContext.newPage();
    page.setDefaultTimeout(0); // disable timeouts

    // Load page
    log.info("script.pageLoad");
    await page.goto("https://www.startpage.com/", {waitUntil: waitEvent});
    await pages.waitForNetworkIdleMax(page, waitNetworkMilliseconds);
    log.info("script.pageLoaded");

    // Issue query
    log.info("script.query");
    const input = await page.locator('#q');
    await input.focus();
    await input.fill(query);
    await Promise.all([
      page.waitForNavigation({url: '**/search'}),
      page.keyboard.press('Enter')
    ]);
    log.info("script.queried");

    // Switch to image search
    log.info("script.imageQuery");
    await Promise.all([
      page.waitForNavigation(),
      page.locator('form[action="/sp/search"] button:has-text("Images"):visible').click()
    ]);
    log.info("script.imageQueried");

    for (let pageNumber = 1; pageNumber < 10; pageNumber += 1) {
      const pageImages = await page.evaluate(() => {
        const pageImages = [];
        const imageContainers = Array.from(document.querySelectorAll('.image-container'));
        for (const imageContainer of imageContainers) {
          imageContainer.click();
          const img = document.querySelector('.expanded-image-container img');
          const proxyImgUrl = new URL(img.src);
          const imgUrl = proxyImgUrl.searchParams.get('piurl');

          const link = document.querySelector('.expanded-details-link > a');
          const linkUrl = link.href;

          pageImages.push([imgUrl, linkUrl]);
        }
        return pageImages;
      });
      console.log(pageImages);

      break; // TODO
    }

    // Take snapshot
    await pages.takeSnapshot(page, optionsSnapshot);
    log.info("script.done");
    return true;
  }
};

