import { Selector } from 'testcafe';

fixture('Wikipedia Random Page Test')
  .page('https://en.wikipedia.org/wiki/Special:Random');

test('Follow first Wikipedia links until Philosophy or loop', async (t) => {
  const visitedPages = new Set<string>();
  let currentPage = '';
  let chainLength = 0;
  const maxIterations = 100; // Safety limit

  // Helper function to get page title
  const getTitleText = async (testController: typeof t) => {
    const title = Selector('#firstHeading');
    await testController.expect(title.exists).ok({ timeout: 10000 });
    return await title.innerText;
  };

  // Helper function to get first valid link
  const getFirstValidLink = async (testController: typeof t) => {
    const content = Selector('#mw-content-text');
    await testController.expect(content.exists).ok({ timeout: 10000 });

    const firstValidLink = await content
      .find('p a')
      .filter((node) => {
        const href = node.getAttribute('href');
        return (
          !node.closest('i') &&
          !node.closest('sup') &&
          !node.closest('.infobox') &&
          href !== null &&
          href.startsWith('/wiki/')
        );
      })
      .nth(0);
    
    await testController.expect(firstValidLink.exists).ok({ timeout: 10000 });
    return firstValidLink;
  };

  // Main loop - follow links until Philosophy or loop
  while (chainLength < maxIterations) {
    // Get current page title
    currentPage = await getTitleText(t);
    console.log(`Step ${chainLength + 1}: ${currentPage}`);

    // Check if we reached Philosophy
    if (currentPage.toLowerCase() === 'philosophy') {
      console.log(`\n✓ Reached Philosophy in ${chainLength} steps!`);
      console.log(`Chain length: ${chainLength}`);
      break;
    }

    // Check for loop (already visited this page)
    if (visitedPages.has(currentPage)) {
      console.log(`\n✗ Loop detected at "${currentPage}"`);
      console.log(`Chain length before loop: ${chainLength}`);
      break;
    }

    // Mark current page as visited
    visitedPages.add(currentPage);

    // Get and click first valid link
    const link = await getFirstValidLink(t);
    await t.click(link);

    // Wait for navigation
    await t.wait(2000);

    chainLength++;
  }

  // Log final results
  console.log('\n=== Test Results ===');
  console.log(`Total pages visited: ${visitedPages.size}`);
  console.log(`Final chain length: ${chainLength}`);
  console.log(`Visited pages: ${Array.from(visitedPages).join(' → ')}`);

  // Assert that we made progress
  await t.expect(chainLength).gt(0);
});
