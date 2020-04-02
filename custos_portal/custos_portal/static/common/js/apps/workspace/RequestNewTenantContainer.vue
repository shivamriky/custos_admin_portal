<template>
    <div>
        <div class="row">
            <div class="col">
                <h1 class="h4 mb-4">New Tenant Request Form</h1>
            </div>
        </div>
        <div>
            <b-form @submit="onSubmit" method="post">
                <b-form-group
                        id="fieldset-1"
                        description=""
                        label="Client Name"
                        label-for="client-name"
                        :invalid-feedback="invalidFeedback"
                        :valid-feedback="validFeedback"
                >
                    <b-form-input
                            id="client-name"
                            name="client-name"
                            v-model="form.client_name"
                            :state="!$v.form.client_name.$invalid"
                            trim>
                    </b-form-input>
                </b-form-group>
                <b-form-group
                        id="fieldset-1"
                        description=""
                        label="Requester Email"
                        label-for="requester-email"
                        :invalid-feedback="invalidFeedback"
                        :valid-feedback="validFeedback"
                >
                    <b-form-input
                            id="requester-email"
                            name="requester-email"
                            v-model="form.requester_email"
                            :state="!$v.form.requester_email.$invalid"
                            type="email"
                            trim>
                    </b-form-input>
                </b-form-group>

                <b-form-group
                        id="fieldset-1"
                        description=""
                        label="Admin Username"
                        label-for="admin-username"
                        :invalid-feedback="invalidFeedback"
                        :valid-feedback="validFeedback"
                >
                    <b-form-input
                            id="admin-username"
                            name="admin-username"
                            v-model="form.admin_username"
                            :state="!$v.form.admin_username.$invalid"
                            trim>
                    </b-form-input>
                </b-form-group>
                <b-form-row>
                    <b-col>
                        <b-form-group
                                id="fieldset-1"
                                description=""
                                label="Admin First Name"
                                label-for="admin-first-name"
                                :invalid-feedback="invalidFeedback"
                                :valid-feedback="validFeedback"
                        >
                            <b-form-input
                                    id="admin-first-name"
                                    name="admin-first-name"
                                    v-model="form.admin_first_name"
                                    :state="!$v.form.admin_first_name.$invalid"
                                    trim>
                            </b-form-input>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                                id="fieldset-1"
                                description=""
                                label="Admin Last Name"
                                label-for="admin-last-name"
                                :invalid-feedback="invalidFeedback"
                                :valid-feedback="validFeedback"
                        >
                            <b-form-input
                                    id="admin-last-name"
                                    name="admin-last-name"
                                    v-model="form.admin_last_name"
                                    :state="!$v.form.admin_last_name.$invalid"
                                    trim>
                            </b-form-input>
                        </b-form-group>
                    </b-col>
                </b-form-row>

                <b-form-group
                        id="fieldset-1"
                        description=""
                        label="Admin Email"
                        label-for="admin-email"
                        :invalid-feedback="invalidFeedback"
                        :valid-feedback="validFeedback"
                >
                    <b-form-input
                            id="admin-email"
                            name="admin-email"
                            v-model="form.admin_email"
                            type="email"
                            :state="!$v.form.admin_email.$invalid"
                            trim>
                    </b-form-input>
                </b-form-group>

                <b-form-group
                        id="fieldset-1"
                        description=""
                        label="Admin Password"
                        label-for="admin-password"
                        :invalid-feedback="invalidFeedback"
                        :valid-feedback="validFeedback"
                >
                    <b-input type="password"
                             id="admin-password"
                             name="admin-password"
                             aria-describedby="password-help-block"
                             v-model="form.admin_password"
                             :state="!$v.form.admin_password.$invalid"
                             trim></b-input>
                    <b-form-text id="password-help-block">
                        Your password must be at least 8 characters long, and must contain letters and numbers, and must
                        at least one special character.
                    </b-form-text>
                </b-form-group>


                <b-form-row>
                    <b-col>
                        <b-form-group
                                id="fieldset-1"
                                description=""
                                label="Primary contact"
                                label-for="primary-contact"
                                :invalid-feedback="invalidFeedback"
                                :valid-feedback="validFeedback"
                        >
                            <b-form-input
                                    id="primary-contact"
                                    name="primary-contact"
                                    v-model="form.primary_contact"
                                    :state="!$v.form.primary_contact.$invalid"
                                    type="tel"
                                    trim>
                            </b-form-input>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                                id="fieldset-1"
                                description=""
                                label="Secondary Contact"
                                label-for="secondary-contact"
                                :invalid-feedback="invalidFeedback"
                                :valid-feedback="validFeedback"
                        >
                            <b-form-input
                                    id="secondary-contact"
                                    name="secondary-contact"
                                    v-model="form.secondary_contact"
                                    :state="!$v.form.secondary_contact.$invalid"
                                    trim>
                            </b-form-input>
                        </b-form-group>
                    </b-col>
                </b-form-row>
                <div v-for="(redirect_uri, index) in form.redirect_uris">
                    <b-form-row class="align-items-center">
                        <b-col>
                            <b-form-group
                                    id="fieldset-1"
                                    description=""
                                    label="Redirect URI"
                                    label-for="redirect-uri"
                                    :invalid-feedback="invalidFeedback"
                                    :valid-feedback="validFeedback"
                            >
                                <b-input-group>
                                    <b-form-input
                                            id="redirect-uri"
                                            name='redirect-uri'
                                            v-model="form.redirect_uris[index]"
                                            :state="!$v.form.redirect_uris.$each[index].$invalid"
                                            type="url"
                                            trim>
                                    </b-form-input>
                                    <b-input-group-append>
                                        <b-button @click="deleteRedirectUri(index)">Delete URI</b-button>
                                        <b-button @click="addRedirectUri(index)">Add another URI</b-button>

                                    </b-input-group-append>
                                </b-input-group>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                </div>
                <b-form-group label="Scope:">
                    <b-form-checkbox-group
                            id="scope"
                            v-model="form.scope"
                            :options="scopeOptions"
                            name="scope"
                    ></b-form-checkbox-group>
                </b-form-group>
                <b-form-group
                        id="fieldset-1"
                        description=""
                        label="Domain"
                        label-for="domain"
                        :invalid-feedback="invalidFeedback"
                        :valid-feedback="validFeedback"
                >
                    <b-form-input
                            id="domain"
                            v-model="form.domain"
                            :state="!$v.form.domain.$invalid"
                            placeholder="idp.htrc.indiana.edu"
                            trim>
                    </b-form-input>
                </b-form-group>
                <b-form-group
                        id="fieldset-1"
                        description=""
                        label="Client URI"
                        label-for="client-uri"
                        :invalid-feedback="invalidFeedback"
                        :valid-feedback="validFeedback"
                >
                    <b-form-input
                            id="client-uri"
                            v-model="form.client_uri"
                            :state="!$v.form.client_uri.$invalid"
                            trim>
                    </b-form-input>
                </b-form-group>
                <b-form-group
                        id="fieldset-1"
                        description=""
                        label="Logo URI"
                        label-for="logo-uri"
                        :invalid-feedback="invalidFeedback"
                        :valid-feedback="validFeedback"
                >
                    <b-form-input
                            id="logo-uri"
                            v-model="form.logo_uri"
                            :state="!$v.form.logo_uri.$invalid"
                            type="url"
                            trim>
                    </b-form-input>
                </b-form-group>

                <b-form-group
                        id="fieldset-1"
                        description="(At least 15 characters long) Provide description of the new tenant and any other comments here."
                        label="Comment"
                        label-for="comment"
                        :invalid-feedback="invalidFeedback"
                        :valid-feedback="validFeedback"
                >
                    <b-form-textarea
                            id="comment"
                            rows="3"
                            textarea
                            v-model="form.comment"
                            :state="!$v.form.comment.$invalid"
                            trim>
                    </b-form-textarea>
                </b-form-group>
                <b-form-group label="Application Type">
                    <b-form-radio-group
                            id="application-type"
                            v-model="form.application_type"
                            :options="application_typeOptions"
                            name="application-type"
                    ></b-form-radio-group>
                </b-form-group>
                <b-button  v-b-modal.modal-1 :disabled="isSubmitDisabled" type="submit" variant="primary">Submit</b-button>

            </b-form>
        </div>
    </div>
</template>

<script>
    import {email, required, url, minLength} from "vuelidate/lib/validators";

    export default {
        computed: {
            state() {
                return this.name.length >= 4 ? true : false
            },
            invalidFeedback() {
                return ''
            },
            validFeedback() {
                return ''
            },
            isSubmitDisabled() {
                return this.$v.form.$invalid;
            }
        },
        data() {
            return {
                form: {
                    client_name: "",
                    requester_email: "",
                    admin_username: "",
                    admin_first_name: "",
                    admin_last_name: "",
                    admin_email: "",
                    admin_password: "",
                    primary_contact: "",
                    secondary_contact: "",
                    redirect_uris: [""],
                    scope: [],
                    domain: "",
                    client_uri: "",
                    logo_uri: "",
                    application_type: "",
                    comment: ""
                },
                scopeOptions: [
                    {text: "openId", value: "openid"},
                    {text: "email", value: "email"},
                    {text: "profile", value: "profile"},
                    {text: "org.cilogon.userinfo", value: "org.cilogon.userinfo"},
                ],
                application_typeOptions: [
                    {text: "web", value: "web"}
                ]
            }
        },
        validations: {
            form: {
                client_name: {required},
                requester_email: {required, email},
                admin_username: {required},
                admin_first_name: {required},
                admin_last_name: {required},
                admin_email: {required},
                admin_password: {
                    required,
                    strongPassword(admin_password) {
                        return (
                            /[a-z]/.test(admin_password) && // checks for a-z
                            /[0-9]/.test(admin_password) && // checks for 0-9
                            /\W|_/.test(admin_password) && // checks for special char
                            admin_password.length >= 8
                        );
                    }
                },
                primary_contact: {required},
                secondary_contact: {},
                scope: {required},
                domain: {
                    required,
                    validDomain(domain) {
                    return (
                        /^((?!-))(xn--)?[a-z0-9][a-z0-9-_]{0,61}[a-z0-9]{0,}\.?((xn--)?([a-z0-9\-.]{1,61}|[a-z0-9-]{1,30})\.?[a-z]{2,})$/.test(domain)
                    )
                    }},
                client_uri: {required},
                logo_uri: {url},
                application_type: {required},
                redirect_uris: {
                    $each: {
                        required, url
                    }
                },
                comment: {required, minLength: minLength(15)}
            }
        },
        methods: {
            onSubmit(event) {
                if(this.$v.form.invalid){
                    console.log("Please fix the errors");
                    event.preventDefault();
                    event.preventDefault();
                }
            },
            addRedirectUri: function () {
                this.form.redirect_uris.push("");
            },
            // TODO check whether 1 redirect URI is there
            deleteRedirectUri: function (index) {
                console.log(index);
                this.form.redirect_uris.splice(index, 1);
            }
        }
    }
</script>