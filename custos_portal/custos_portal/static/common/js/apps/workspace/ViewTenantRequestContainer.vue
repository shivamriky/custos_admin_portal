<template>
    <div>
        <div class="row">
            <div class="col">
                <h1 class="h4 mb-4">Tenant Request Details</h1>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <div class="card border-default">
                    <div class="card-body">
                        <table class="table">
                            <tbody>
                            <tr>
                                <th scope="row">Request Id</th>
                                <td>
                                    <div> {{tenantRequestId}}</div>
                                </td>
                            </tr>
                            <tr>
                                <th scope="row">Client Name</th>
                                <td>
                                    <div> {{request.client_name}}</div>
                                </td>
                            </tr>
                            <tr>
                                <th scope="row">Requester Email</th>
                                <td>{{request.requester_email}}</td>
                            </tr>
                            <tr>
                                <th scope="row">Admin Username</th>
                                <td>{{request.admin_username}}</td>
                            </tr>
                            <tr>
                                <th scope="row">Admin Name</th>
                                <td>{{request.admin_first_name}} {{ " " }} {{request.admin_last_name}}</td>
                            </tr>
                            <tr>
                                <th scope="row">Primary contact</th>
                                <td>{{request.primary_contact}}</td>
                            </tr>
                            <tr>
                                <th scope="row">Secondary contact</th>
                                <td>{{request.secondary_contact}}</td>
                            </tr>
                            <tr>
                                <th scope="row">Redirect URI Name</th>
                                <td>{{request.redirect_uris}}</td>
                            </tr>
                            <tr>
                                <th scope="row">Scope</th>
                                <td>{{request.scope}}</td>
                            </tr>
                            <tr>
                                <th scope="row">Domain</th>
                                <td>{{request.domain}}</td>
                            </tr>
                            <tr>
                                <th scope="row">Client URI</th>
                                <td>{{request.client_uri}}</td>
                            </tr>
                            <tr>
                                <th scope="row">Comment</th>
                                <td>{{request.comment}}</td>
                            </tr>


                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            tenantRequestId: {
                required: true
            }
        },
        data() {
            return {
                request: {
                    client_name: "Test Client",
                    requester_email: "tmp@gmail.com",
                    admin_username: "airavata_admin",
                    admin_first_name: "Shivam",
                    admin_last_name: "Rastogi",
                    admin_email: "shivam@airavata.com",
                    primary_contact: "51651",
                    secondary_contact: "5545",
                    redirect_uris: ["http://tst.com"],
                    scope: ["test"],
                    domain: "google.com",
                    client_uri: "http://tst.com",
                    logo_uri: "http://tst.com",
                    application_type: "web",
                    comment: "Testing the page"
                }
            }
        }
    }
</script>