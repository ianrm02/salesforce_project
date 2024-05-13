Field Session:
Data Harmonization for State and Country
Information
Proposed for Colorado School of Mines Field Session, Spring 2024
by Jens Schutt, VP Platform Engineering for Globalization at Salesforce

About Salesforce:
Salesforce is cloud-based CRM software (What is CRM?). It makes it easier for companies to find more prospects, close more deals, and connect with customers in a whole new way, so they can provide them with amazing service at scale.
Salesforce's comprehensive suite of products, including Einstein, integrates data from diverse sources, enabling seamless collaboration across sales, service, marketing, commerce, and IT functions. Leveraging artificial intelligence across its offerings, Salesforce enhances productivity and fosters personalized customer experiences.

The Project:
Many of our customers utilize a configuration feature within Salesforce where the country and state fields are filled with free-text entries in addresses. Our objective is to develop a utility enabling customers to effortlessly transition to a standardized list of pre-approved state and country codes according to ISO 3166-1.

Success Criteria
1. Achieve maximum conversion of free-text state and country entries into the standardized list.
2. The utility must operate independently without external calls or data sharing with address validation services. It should solely rely on database connectivity.
3. Design a user interface allowing users to review and confirm dataset changes before updating data. Given the large datasets typically managed by our clients, this confirmation process must be highly efficient to minimize user effort.
4. Ensure the reusability of user-approved conversion rules. The utility should facilitate testing in non-production environments, allowing users to apply conversion rules seamlessly to their production environment.
 
Technologies
- Java or another mainstream language
- Relational Database
- Open to additional recommendations and suggestions. 
- Heroku