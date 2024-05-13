Java + postgres?

- [ ] Create general project design
- [ ] Get (or create) state/country data
- [ ] Design the database
- [ ] Convert the finished database to XML
- [ ] Create minimum effective GUI for demonstration of states/country lists
- [ ] Convert the finished
- [ ] Create graphical interface for updating database
- [ ] Create a testing environment for users

Questions
- [ ] Do you have a dataset for us to use or are we expected to curate the data? Any hints on where to look?
- [ ] Do you want a graphical interface to confirm the users changes? What changes are you expecting users to make to the database?
- [ ] Could you clarify our understanding of this goal: "Ensure the reusability of user-approved conversion rules. The utility should facilitate testing in non-production environments, allowing users to apply conversion rules seamlessly to their production environment." We are assuming this means you want a testing environment to test those user changes before they are confirmed and then it should be easy to push these changes to the true environment. 
- [ ] Also, each client should have their own database so that they do not need to stick to the default one we will create. This could be done with branches (each client has their own database similar to the original one) or one large database that all clients share and when they make a change it adds a database for that company.