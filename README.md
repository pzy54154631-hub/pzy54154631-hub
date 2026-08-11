<div align="center">

# laipeng

*an undergraduate student studying in the United States*

`multimodal reasoning` · `uncertainty-aware inference` · `object-centric AI`

<br>

**Building systems that know what they see, what they do not know, and when they should ask.**

</div>

<br>

## Research directions

<table>
  <tr>
    <td width="33%" valign="top">
      <h3>Referents &amp; routing</h3>
      <p>Separating ambiguity, uncertainty, and answerability in multimodal systems.</p>
    </td>
    <td width="33%" valign="top">
      <h3>Objects &amp; residuals</h3>
      <p>Preserving structured hypotheses instead of collapsing them too early.</p>
    </td>
    <td width="33%" valign="top">
      <h3>Calibration &amp; evaluation</h3>
      <p>Designing diagnostics that reveal why an inference pipeline succeeds or fails.</p>
    </td>
  </tr>
</table>

## Selected work

<table>
  <tr>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/pzy54154631-hub/ambiguity-is-not-one-scalar">Ambiguity Is Not One Scalar</a></h3>
      <p>A referent-aware VQA router over <strong>ANSWER / CLARIFY / ABSTAIN</strong>.</p>
      <p><strong>20/22</strong> audited low-score focus-ambiguity false negatives recovered by referent enumeration, versus <strong>0/22</strong> for answer self-consistency.</p>
      <sub>VQA · selective prediction · calibration</sub>
    </td>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/pzy54154631-hub/pw-ofpc">PW-OFPC</a></h3>
      <p>Precision-weighted object-file predictive coding for abstract visual reasoning.</p>
      <p>Public-RAVEN macro accuracy: <strong>0.537 → 0.857</strong> across the reported inference ladder.</p>
      <sub>object files · predictive coding · RAVEN</sub>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/pzy54154631-hub/Scale-Is-Not-Symmetric">Scale Is Not Symmetric</a></h3>
      <p>Directional scale errors in ChartQA and interference-aware LoRA merging.</p>
      <p>Includes the MIRAGE rank-wise adapter-merging implementation and claim-to-artifact checks.</p>
      <sub>ChartQA · LoRA merging · diagnostics</sub>
    </td>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/pzy54154631-hub/F-ARCS">F-ARCS</a></h3>
      <p>Factorized candidate sharing across ChartQA and Raven-style tasks.</p>
      <p>A protocol-first release documenting both the architecture and a hypothesis that did not meet its promotion criteria.</p>
      <sub>candidate comparison · negative results · reproducibility</sub>
    </td>
  </tr>
</table>

## In progress

**[AAAI-2027-Fusion](https://github.com/pzy54154631-hub/AAAI-2027-Fusion)** explores how referent-aware VQA routing and uncertainty-preserving object-file reasoning can be combined without collapsing their distinct failure mechanisms.

---

<div align="center">
  <sub>Research artifacts include explicit evidence boundaries, reproducibility notes, and known limitations.</sub>
</div>
