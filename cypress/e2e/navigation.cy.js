describe('SecureAI Notes App E2E', () => {
  it('loads the app and runs an AI suggestion', () => {
    cy.visit('/');
    cy.contains('h1', 'SecureAI Notes');
    cy.get('#note').should('be.visible').type('This is a test note.');
    cy.get('#analyzeBtn').click();
    // Wait for spinner to hide and suggestions to render
    cy.get('#loading').should('not.be.visible');
    cy.get('#suggestions').should('contain', 'Summary:');
  });
});
