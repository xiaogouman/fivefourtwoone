<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/warehouses">
	<html>
	  <body>
	  	<h1>query-1(a)</h1>
	  	<ul>
			<xsl:for-each select="warehouse">
	            <xsl:if test="address[country='Singapore']">
					<li>warehouse: <xsl:value-of select="name"/>
						<ul>
							<xsl:for-each select="items/item">
								<xsl:if test="qty > 975">
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