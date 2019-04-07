<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/warehouses">
	<html>
	  <body>
	  	<h1>query-3(c)</h1>
	  	<p><xsl:value-of select="sum(//warehouse[address/country='Indonesia']/items/item[name='Sunscreen']/qty)"/></p>
	</body>
  </html>
</xsl:template>

</xsl:stylesheet>