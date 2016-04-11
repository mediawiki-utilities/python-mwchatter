import unittest
import wikichatter.signatureutils as signatureutils
import wikichatter.mwparsermod as mwpm


class SignatureUtilsTest(unittest.TestCase):

    def test_identifies_multiple_signatures(self):
        sigs = ['[[User:Dee03z|Dee03z]] ([[User talk:Dee03z|talk]]) 16:39, 27 April 2012 (UTC)\n',
                '[[User:SarahStierch|Sarah]] ([[User talk:SarahStierch|talk]]) 16:56, 27 April 2012 (UTC)\n',
                '[[User:AbigailAbernathy|<font color="darkred">''A Wild Abigail Appears!''</font>]] [[User talk:AbigailAbernathy|<font color="slate"><sub>Capture me.</sub></font>]] [[Special:EmailUser/AbigailAbernathy|<font color="seagreen"><sub>Flee.</sub></font>]] 18:51, 27 April 2012 (UTC)\n',
                '[[User:Nathan2055|Nathan2055]][[User Talk:Nathan2055|<sup>talk</sup>]] 22:21, 27 April 2012 (UTC)\n',
                '[[User:SarahStierch|Sarah]] ([[User talk:SarahStierch|talk]]) 22:25, 27 April 2012 (UTC)\n',
                '[[User:Mir Almaat 1 S1|RDF Energia]] [[User talk:Mir Almaat 1 S1||<span style="font-size: 1.2em;color:transparent;text-shadow:gold 0em 0.2em 0.02em;">  ☏</span>]] 05:43, 27 April 2012 (UTC)\n',
                '[[User:McDoobAU93|<span style="color:#000080">McDoob</span>]][[User talk:McDoobAU93|<span style="color:#cc5500">AU</span>]][[Special:Contributions/McDoobAU93|<span style="color:#000080">93</span>]] 01:31, 29 April 2012 (UTC)\n',
                '[[User:Charlesdrakew|Charles]] ([[User talk:Charlesdrakew|talk]]) 22:28, 28 April 2012 (UTC)\n',
                '[[User:Tlqk56|Tlqk56]] ([[User talk:Tlqk56|talk]]) 04:19, 29 April 2012 (UTC)\n']
        wikitext = ''.join(sigs)
        code = mwpm.parse(wikitext)

        detected_sigs = signatureutils.extract_signatures(code)

        self.assertEqual(len(sigs), len(detected_sigs))
        for sig in detected_sigs:
            self.assertIn(str(sig['wikicode']), sigs)

    def test_identifies_correct_user(self):
        template = '[[User:{user}|{user}]] ([[User talk:{user}|talk]]) 16:39, 27 April 2012 (UTC)'
        user = "Some_Person"
        wikitext = template.format(user=user)
        code = mwpm.parse(wikitext)

        detected_sigs = signatureutils.extract_signatures(code)

        self.assertEqual(1, len(detected_sigs))
        self.assertEqual(user, detected_sigs[0]['user'])

    def test_identifies_correct_time(self):
        template = '[[User:Some_Person|Some_Person]] ([[User talk:Some_Person|talk]]) 16:39, {timestamp}'
        timestamp = "16:39, 27 April 2012 (UTC)"
        wikitext = template.format(timestamp=timestamp)
        code = mwpm.parse(wikitext)

        detected_sigs = signatureutils.extract_signatures(code)

        self.assertEqual(1, len(detected_sigs))
        self.assertEqual(timestamp, detected_sigs[0]['timestamp'])

    def test_identifies_backwards_signature(self):
        wikitext = ("Hi i wanted to make sure i didnt plagiarize. What are the rules",
                    " on using others' information on wikipedia. Can i paraphrase it",
                    " as long as I cite the link? Can anyone get sued from ",
                    "paraphrasing with citation01:52, 20 September 2013 (UTC)  ",
                    '<small><span class="autosigned">— Preceding ',
                    '[[Wikipedia:Signatures|unsigned]] comment added by ',
                    '[[User:Fishingforspecies|Fishingforspecies]] ',
                    '([[User talk:Fishingforspecies|talk]] • ',
                    '[[Special:Contributions/Fishingforspecies|contribs]]) ',
                    '</span></small>')
        wcode = mwpm.parse(wikitext)

        detected_sigs = signatureutils.extract_signatures(wcode)

        self.assertEqual(1, len(detected_sigs))

    def test_identifies_hhmm_MMM_DD_YYYY_format(self):
        wikitext = ('the first is also illegible on Netscape, but you can tell'
                    ' what was intended; the second is perfectly legible.  '
                    '[[User:Michael Hardy|Michael Hardy]] 18:45 Mar 10, 2003 (UTC)\n')
        wcode = mwpm.parse(wikitext)

        detected_sigs = signatureutils.extract_signatures(wcode)

        self.assertEqual(1, len(detected_sigs))

    def test_identifies_hhmmss_YYYYMMDD_format(self):
        wikitext = ' in my opinion. [[User:Nahaj|Nahaj]] 01:54:53, 2005-09-08 (UTC) '
        wcode = mwpm.parse(wikitext)

        detected_sigs = signatureutils.extract_signatures(wcode)

        self.assertEqual(1, len(detected_sigs))
