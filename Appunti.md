
# From: https://www.codeproject.com/Tips/833087/X-SSL-Certificates-With-Custom-Extensions-2
# Create a X509 Cert with Custom Extension

  - vim /etc/ssl/openssl.cfg and add the followings under [v3_req] and save:
  
		OID=critical,ASN1:UTF8String:My custom extension's value
		OID=ASN1:UTF8String:My custom extension's value

  -  Generate server key: 
				    `openssl genrsa -des3 -out server.key 1024`
  
  -  Create certificate signing request: 
			`openssl req -new -key server.key -out server.csr -config openssl.cfg`

  - Copy key to somewhere temporarily: 
					    `cp server.key server.key.org`
  
  -  Remove the passphrase: 
					    `openssl rsa -in server.key.org -out server.key`

  -  Generate your certificate with standard extensions: 
		  `openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt -extensions v3_req -extfile openssl.cfg`


# From RFC 8250


# Some fundamental OIDs for x509 MUDURL Extension

IANA has made the following assignments for:
-   **MUDURLExtnModule-2016 ASN.1 module (88)** in the "SMI Security
      for PKIX Module Identifier" registry (1.3.6.1.5.5.7.0.88).

-  **id-pe-mud-url object identifier (25)** from the "SMI Security for
      PKIX Certificate Extension" registry (1.3.6.1.5.5.7.1).

-   **id-pe-mudsigner object identifier (30)** from the "SMI Security for
      PKIX Certificate Extension" registry (1.3.6.1.5.5.7.1.30).

-   **id-ct-mudtype object identifier (41)** from the "SMI Security for
      S/MIME CMS Content Type" registry (1.2.840.113549.1.9.16.1.41).


# MUDURL Extension for x509

The new extension is identified as follows:

	   `<CODE BEGINS>`
	      `MUDURLExtnModule-2016 { iso(1) identified-organization(3) dod(6)`
	                   `internet(1) security(5) mechanisms(5) pkix(7)`
	                   `id-mod(0) id-mod-mudURLExtn2016(88) }`
	       `DEFINITIONS IMPLICIT TAGS ::= BEGIN`

       `-- EXPORTS ALL --`

      `IMPORTS`

        `-- RFC 5912`
        `EXTENSION`
        `FROM PKIX-CommonTypes-2009`
             `{ iso(1) identified-organization(3) dod(6) internet(1)`
               `security(5) mechanisms(5) pkix(7) id-mod(0)`
               `id-mod-pkixCommon-02(57) }`

        `-- RFC 5912`
        `id-ct`
        `FROM PKIXCRMF-2009`
             `{ iso(1) identified-organization(3) dod(6) internet(1)`
               `security(5)  mechanisms(5) pkix(7) id-mod(0)`
               `id-mod-crmf2005-02(55) }`

        `-- RFC 6268`
        `CONTENT-TYPE`
        `FROM CryptographicMessageSyntax-2010`
          `{ iso(1) member-body(2) us(840) rsadsi(113549)`
            `pkcs(1) pkcs-9(9) smime(16) modules(0) id-mod-cms-2009(58) }`

        `-- RFC 5912`
        `id-pe, Name`
        `FROM PKIX1Explicit-2009`
              `{ iso(1) identified-organization(3) dod(6) internet(1)`
                `security(5) mechanisms(5) pkix(7) id-mod(0)`
                `id-mod-pkix1-explicit-02(51) } ;`

       `--`
       `-- Certificate Extensions`
       `--`

       `MUDCertExtensions EXTENSION ::=`
          `{ ext-MUDURL | ext-MUDsigner, ... }`

       `ext-MUDURL EXTENSION ::=` 
          `{ SYNTAX MUDURLSyntax IDENTIFIED BY id-pe-mud-url }`

       `id-pe-mud-url OBJECT IDENTIFIER ::= { id-pe 25 }`

       `MUDURLSyntax ::= IA5String`

       `ext-MUDsigner EXTENSION ::=`
          `{ SYNTAX MUDsignerSyntax IDENTIFIED BY id-pe-mudsigner }`

       `id-pe-mudsigner OBJECT IDENTIFIER ::= { id-pe 30 }`

       `MUDsignerSyntax ::= Name`

       `--`
       `-- CMS Content Types`
       `--`

       `MUDContentTypes CONTENT-TYPE ::=`
          `{ ct-mud, ... }`

        `ct-mud CONTENT-TYPE ::=`
          `{ -- directly include the content`
            `IDENTIFIED BY id-ct-mudtype }`
          `-- The binary data that is in the form`
          `-- "application/mud+json" is directly encoded as the`
          `-- signed data.  No additional ASN.1 encoding is added.`

       `id-ct-mudtype OBJECT IDENTIFIER ::= { id-ct 41 }`

       `END`
   `<CODE ENDS>`
