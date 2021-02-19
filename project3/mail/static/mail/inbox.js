document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(is_reply=false, pre_fill=null) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // pre-fill fields if email is a reply
  if (is_reply && pre_fill != null) {
    document.querySelector('#compose-recipients').value = pre_fill.recipient;
    document.querySelector('#compose-subject').value = pre_fill.subject;
    document.querySelector('#compose-body').value = pre_fill.body;
  }

  // Send out email
  document.querySelector('#compose-form').onsubmit = () => {
    send_email();
    load_mailbox('sent');
  }
}

function send_email() {
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
  });

  return false;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // get list of emails in the mailbox and for each, displays who email is from, the subject line, and timestamp of the email
  fetch('/emails/' + mailbox)
  .then(response => response.json())
  .then(data => {
    console.log(data);
    data.forEach((email) => {
      const div = document.createElement('div');
      div.className = 'email-div';
      let sender = '<b>From: </b>' + email.sender + '<br/>';
      let subject = '<b>Subject: </b>' + email.subject + '<br/>';
      let timestamp = '<b>Timestamp: </b>' + email.timestamp;
      div.innerHTML = sender + subject + timestamp;

      if (email.read) {
        div.className += ' read';
      } 

      // user taken to a view containing contents of email when user clicks on an email in mailbox
      div.addEventListener('click', () => {
        load_email(email.id, mailbox);
      })

      document.querySelector('#emails-view').append(div);
    })
  });
}

function load_email(email_id, mailbox) {
  fetch('/emails/' + email_id)
  .then(response => response.json())
  .then(email => {
    // clear previous HTML
    const email_view = document.querySelector('#emails-view');
    email_view.innerHTML = '';

    let info_div = document.createElement('div');

    let sender = '<b>From: </b>' + email.sender + '<br/>';
    let recipients = '<b>To: </b>' + email.recipients[0];

    // prepend each additional recipient address with a comma
    if (email.recipients.length > 1) {
      email.recipients.slice(1, email.recipients.length - 1).forEach(recipient => {
        recipients += ', ' + recipient;
      })
    }
    recipients += '<br/>'
    let subject = `<b>Subject: </b>${email.subject}<br/>`;
    let timestamp = `<b>Timestamp: </b>${email.timestamp}<br/>`;

    info_div.innerHTML = sender + recipients + subject + timestamp;
    email_view.append(info_div);

    let reply_button = document.createElement('button');
    reply_button.classList.add("btn", "btn-sm", "btn-outline-primary");
    reply_button.innerHTML = 'Reply';
    reply_button.addEventListener('click', () => {
      // dictionary used to pre-fill fields with content when replying to an email
      pre_fill = {
        recipient: email.sender,
        subject: email.subject.includes("Re:") ? email.subject : `Re: ${email.subject}`,
        body: `On ${email.timestamp} ${email.sender} wrote: ${email.body}`
      }
      compose_email(true, pre_fill);
    })

    let archive_button = document.createElement('button');
    archive_button.classList.add("btn", "btn-sm", "btn-outline-primary");
    if (!email.archived) {
      archive_button.innerHTML = 'Archive Email';
    } else {
      archive_button.innerHTML = 'Unarchive Email';
    }

    archive_button.addEventListener('click', () => {
      toggle_archive(email.id, email.archived);
      location.reload();
      load_mailbox('inbox');
    });

    let button_div = document.createElement('div');
    button_div.append(reply_button);
    button_div.append(archive_button);
    email_view.append(button_div);

    let body_div = document.createElement('div');
    body_div.innerHTML = '<hr>' + email.body;

    email_view.append(body_div);

    if (!email.read) {
      mark_read(email.id);
    }
  })
}

function toggle_archive(email_id, is_archived) {
  fetch('/emails/' + email_id, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !is_archived
    })
  })
}

function mark_read(email_id) {
  fetch('/emails/' + email_id, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
}

