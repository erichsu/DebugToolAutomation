<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" doctype-system="http://www.w3.org/TR/html4/strict.dtd" doctype-public="-//W3C//DTD HTML 4.01//EN" indent="yes" />
	<xsl:template match="/">
<html>
<head>
<title>Automation Tool Test Case Report - <xsl:value-of select="testcase/id"/></title>

</head>
<body>

<xsl:for-each select="testcase/inis/ini">
<table border="1" width="100%" cellpadding="3" cellspacing="0" summary="">
	<tr bgcolor="#ccccff">
	<th align="left" colspan="3">
	<font size="+2"><b><xsl:value-of select="filename"/></b></font>
	</th>
	</tr>
	
	<tr bgcolor="#eeeeee">
	<th>key</th>
	<th>expected</th>
	<th>status</th>
	</tr>
	<xsl:for-each select="conds/cond">
	<tr bgcolor="white">
	<td width="20%"><b><xsl:value-of select="key"/></b></td>
	<td><xsl:value-of select="value"/></td>
	<td>
	<xsl:choose>
	<xsl:when test="status = 'True'"><img alt="succ" src="images/succ.jpg"/></xsl:when>
	<xsl:otherwise><img alt="fail" src="images/fail.jpg"/><xsl:value-of select="status"/></xsl:otherwise>
	</xsl:choose>
	</td>
	</tr>
	</xsl:for-each>

</table>
</xsl:for-each>

</body>
</html>
	</xsl:template>
</xsl:stylesheet>
