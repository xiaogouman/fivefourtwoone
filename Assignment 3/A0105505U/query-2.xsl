<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/warehouses">
	<html>
	  <h1>query-2(b)</h1>
	  <body>
	  <ul>
		<xsl:for-each select="warehouse">
            <xsl:if test="address[country='Singapore'] or address[country='Malaysia']">
				<li>warehouse: <xsl:value-of select="name"/>
				<ul>
					<xsl:for-each select="items/item">
						<xsl:sort select="qty" data-type="number" order="descending"/>
						<xsl:if test="position() = 1">
							<li>item: <xsl:value-of select="name"/>, qty: <xsl:value-of select="qty"/></li>
						</xsl:if>
					</xsl:for-each>
				</ul>
				</li>
			</xsl:if>
		</xsl:for-each>
		</ul>
	</body>
  </html>
</xsl:template>

</xsl:stylesheet>
