from enum import Enum


class JobExperienceTypes(str, Enum):
    INTERN = "Intern"
    JUNIOR = "Junior"
    MID_LEVEL = "Mid-Level"
    SENIOR = "Senior"


class JobExperienceToResendSegmentID(str, Enum):
    INTERN = "e536533e-31c0-4fd1-be01-7b5f082b214c"
    JUNIOR = "5d1e737f-3a54-4a1a-a013-d5873bc761d5"
    MID_LEVEL = "72d8e8ec-4420-4dd4-8847-4da5fb58d1cf"  # SENIOR also maps to this segment ID due to Resend limitations


RESEND_JOB_TEMPLATE_HTML = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html dir="ltr" lang="en">
  <head>
    <meta content="width=device-width" name="viewport" />
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
    <meta name="x-apple-disable-message-reformatting" />
    <meta content="IE=edge" http-equiv="X-UA-Compatible" />
    <meta name="x-apple-disable-message-reformatting" />
    <meta
      content="telephone=no,address=no,email=no,date=no,url=no"
      name="format-detection" />
  </head>
  <body>
    <!--$--><!--html--><!--head--><!--body-->
    <table
      border="0"
      width="100%"
      cellpadding="0"
      cellspacing="0"
      role="presentation"
      align="center">
      <tbody>
        <tr>
          <td>
            <table
              align="center"
              width="100%"
              border="0"
              cellpadding="0"
              cellspacing="0"
              role="presentation"
              style="font-family:-apple-system, BlinkMacSystemFont, &#x27;Segoe UI&#x27;, &#x27;Roboto&#x27;, &#x27;Oxygen&#x27;, &#x27;Ubuntu&#x27;, &#x27;Cantarell&#x27;, &#x27;Fira Sans&#x27;, &#x27;Droid Sans&#x27;, &#x27;Helvetica Neue&#x27;, sans-serif;font-size:1.0769230769230769em;min-height:100%;line-height:155%">
              <tbody>
                <tr>
                  <td>
                    <table
                      align="left"
                      width="100%"
                      border="0"
                      cellpadding="0"
                      cellspacing="0"
                      role="presentation"
                      style="align:left;width:100%;padding-left:0px;padding-right:0px;line-height:155%;max-width:600px;font-family:-apple-system, BlinkMacSystemFont, &#x27;Segoe UI&#x27;, &#x27;Roboto&#x27;, &#x27;Oxygen&#x27;, &#x27;Ubuntu&#x27;, &#x27;Cantarell&#x27;, &#x27;Fira Sans&#x27;, &#x27;Droid Sans&#x27;, &#x27;Helvetica Neue&#x27;, sans-serif">
                      <tbody>
                        <tr>
                          <td>
                            <h1
                              style="margin:0;padding:0;font-size:2.25em;line-height:1.44em;padding-top:0.389em;font-weight:600;color:#5436ce;text-align:center">
                              <span>jobseekr.</span>
                            </h1>
                            <p
                              style="margin:0;padding:0;font-size:1em;padding-top:0.5em;padding-bottom:0.5em;text-align:center">
                              <br />
                            </p>
                            <h3
                              style="margin:0;padding:0;font-size:1.4em;line-height:1.08em;padding-top:0.389em;font-weight:600;text-align:left">
                              <span>Hi,</span>
                            </h3>
                            <p
                              style="margin:0;padding:0;font-size:1em;padding-top:0.5em;padding-bottom:0.5em;text-align:left">
                              <br />
                            </p>
                            <p
                              style="margin:0;padding:0;font-size:1em;padding-top:0.5em;padding-bottom:0.5em;text-align:left">
                              <span
                                >This is your daily job report! Today, we have
                                found </span
                              ><strong>{{{NUM_OF_JOBS}}}</strong
                              ><span> jobs that best match your skillset!</span>
                            </p>
                            <p
                              style="margin:0;padding:0;font-size:1em;padding-top:0.5em;padding-bottom:0.5em;text-align:left">
                              <br />
                            </p>
                            <p
                              style="margin:0;padding:0;font-size:1em;padding-top:0.5em;padding-bottom:0.5em;text-align:left">
                              <span>Here are </span
                              >{{{NUM_OF_JOBS_IN_EMAIL}}}<span>
                                recently found job(s):</span
                              >
                            </p>
                            <p
                              style="margin:0;padding:0;font-size:1em;padding-top:0.5em;padding-bottom:0.5em;text-align:left">
                              {{{JOB_1}}}
                            </p>
                            <p
                              style="margin:0;padding:0;font-size:1em;padding-top:0.5em;padding-bottom:0.5em">
                              {{{JOB_2}}}
                            </p>
                            <p
                              style="margin:0;padding:0;font-size:1em;padding-top:0.5em;padding-bottom:0.5em">
                              {{{JOB_3}}}
                            </p>
                            <p
                              style="margin:0;padding:0;font-size:1em;padding-top:0.5em;padding-bottom:0.5em">
                              {{{JOB_4}}}
                            </p>
                            <p
                              style="margin:0;padding:0;font-size:1em;padding-top:0.5em;padding-bottom:0.5em">
                              {{{JOB_5}}}
                            </p>
                            <p
                              style="margin:0;padding:0;font-size:1em;padding-top:0.5em;padding-bottom:0.5em">
                              <br />
                            </p>
                            <p
                              style="margin:0;padding:0;font-size:1em;padding-top:0.5em;padding-bottom:0.5em">
                              <span
                                >To view all of today&#x27;s found jobs, visit
                                your </span
                              ><span
                                ><a
                                  href="{{{DASHBOARD}}}"
                                  rel="noopener noreferrer nofollow"
                                  style="color:#0670DB;text-decoration-line:none;text-decoration:underline"
                                  target="_blank"
                                  >dashboard</a
                                ></span
                              ><span>!</span>
                            </p>
                            <p
                              style="margin:0;padding:0;font-size:1em;padding-top:0.5em;padding-bottom:0.5em">
                              <br />
                            </p>
                            <p
                              style="margin:0;padding:0;font-size:1em;padding-top:0.5em;padding-bottom:0.5em">
                              <span
                                >Not what you are looking for? Visit your </span
                              ><span
                                ><a
                                  href="{{{DASHBOARD}}}"
                                  rel="noopener noreferrer nofollow"
                                  style="color:#0670DB;text-decoration-line:none;text-decoration:underline"
                                  target="_blank"
                                  >dashboard</a
                                ></span
                              ><span> and change your preferences!</span>
                            </p>
                            <p
                              style="margin:0;padding:0;font-size:1em;padding-top:0.5em;padding-bottom:0.5em">
                              <br />
                            </p>
                            <table
                              align="center"
                              width="100%"
                              border="0"
                              cellpadding="0"
                              cellspacing="0"
                              role="presentation"
                              class="node-footer"
                              style="font-size:0.8em">
                              <tbody>
                                <tr>
                                  <td>
                                    <hr
                                      class="divider"
                                      style="width:100%;border:none;border-top:1px solid #eaeaea;padding-bottom:1em;border-width:2px" />
                                    <p
                                      style="margin:0;padding:0;font-size:1em;padding-top:0.5em;padding-bottom:0.5em">
                                      <span
                                        >You are receiving this email because
                                        you opted in via our site.</span
                                      ><br /><br /><span
                                        >Want to change how you receive these
                                        emails?</span
                                      ><br /><span>You can </span
                                      ><span
                                        ><a
                                          href="{{{RESEND_UNSUBSCRIBE_URL}}}"
                                          rel="noopener noreferrer nofollow"
                                          ses:no-track="true"
                                          style="color:#0670DB;text-decoration-line:none;text-decoration:underline"
                                          target="_blank"
                                          >unsubscribe from this list</a
                                        ></span
                                      ><span>.</span>
                                    </p>
                                    <p
                                      style="margin:0;padding:0;font-size:1em;padding-top:0.5em;padding-bottom:0.5em">
                                      <span
                                        >*Note - unsubscribing directly from
                                        this email might not properly reflect
                                        your preferences in your dashboard. To
                                        unsubscribe and properly reflect your
                                        preferences, visit your </span
                                      ><span
                                        ><a
                                          href="{{{DASHBOARD}}}"
                                          rel="noopener noreferrer nofollow"
                                          style="color:#0670DB;text-decoration-line:none;text-decoration:underline"
                                          target="_blank"
                                          >dashboard</a
                                        ></span
                                      ><span>.</span>
                                    </p>
                                    <p
                                      style="margin:0;padding:0;font-size:1em;padding-top:0.5em;padding-bottom:0.5em">
                                      <span>jobseekr.dev</span>
                                    </p>
                                  </td>
                                </tr>
                              </tbody>
                            </table>
                            <p
                              style="margin:0;padding:0;font-size:1em;padding-top:0.5em;padding-bottom:0.5em">
                              <br />
                            </p>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>
    <!--/$-->
  </body>
</html>
"""

JOB_SEEKR_DASHBOARD = "https://jobseekr.dev/dashboard"

STATUS_CODE_200 = 200

GROQ_SYSTEM_PROMPT = """
You are a specialized JSON parser. Extract resume data into the exact format requested.
Do not include markdown code blocks (```json).
Do not include any introductory or concluding text.
Return ONLY the raw JSON string.
"""

GROQ_PARSE_TEXT_PROMPT = """
Extract structured tech resume data as JSON with:
- skills (list)
- experience level (string and it can only be: 'Intern', 'Junior', 'Mid-Level', or 'Senior'. This is based off of information from the resume, such as if they graduated or YOE working in the tech industry)


Return ONLY valid JSON in this exact format:

{{
  "skills": [string],
  "experience_level" string
}}

Resume:
{}
"""
