<template>
    <div >
        <b-form @submit="onSubmit">
            <b-form-group
                    id="fieldset-1"
                    description=""
                    label="Client Name"
                    label-for="input-1"
                    :invalid-feedback="invalidFeedback"
                    :valid-feedback="validFeedback"
            >
                <b-form-input
                        id="input-1"
                        v-model="form.client_name"
                        :state="!$v.form.client_name.$invalid"
                        trim>
                </b-form-input>
            </b-form-group>
            <b-form-group
                    id="fieldset-1"
                    description=""
                    label="Requester Email"
                    label-for="input-1"
                    :invalid-feedback="invalidFeedback"
                    :valid-feedback="validFeedback"
            >
                <b-form-input
                        id="input-1"
                        v-model="form.requester_email"
                        :state="!$v.form.requester_email.$invalid"
                        trim>
                </b-form-input>
            </b-form-group>

            <b-form-group
                    id="fieldset-1"
                    description=""
                    label="Admin Username"
                    label-for="input-1"
                    :invalid-feedback="invalidFeedback"
                    :valid-feedback="validFeedback"
            >
                <b-form-input
                        id="input-1"
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
                            label-for="input-1"
                            :invalid-feedback="invalidFeedback"
                            :valid-feedback="validFeedback"
                    >
                        <b-form-input
                                id="input-1"
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
                            label-for="input-1"
                            :invalid-feedback="invalidFeedback"
                            :valid-feedback="validFeedback"
                    >
                        <b-form-input
                                id="input-1"
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
                    label-for="input-1"
                    :invalid-feedback="invalidFeedback"
                    :valid-feedback="validFeedback"
            >
                <b-form-input
                        id="input-1"
                        v-model="form.admin_email"
                        :state="!$v.form.admin_email.$invalid"
                        trim>
                </b-form-input>
            </b-form-group>

            <b-form-group
                    id="fieldset-1"
                    description=""
                    label="Admin Password"
                    label-for="input-1"
                    :invalid-feedback="invalidFeedback"
                    :valid-feedback="validFeedback"
            >
                <b-input type="password"
                        id="text-password"
                        aria-describedby="password-help-block"
                        v-model="form.admin_password"
                        :state="!$v.form.admin_password.$invalid"
                        trim></b-input>
                <b-form-text id="password-help-block">
                    Your password must be 8-20 characters long, and must contain letters and numbers, and must
                    at least one special character.
                </b-form-text>
            </b-form-group>


            <b-form-row>
                <b-col>
                    <b-form-group
                            id="fieldset-1"
                            description=""
                            label="Primary contact"
                            label-for="input-1"
                            :invalid-feedback="invalidFeedback"
                            :valid-feedback="validFeedback"
                    >
                        <b-form-input
                                id="input-1"
                                v-model="form.primary_contact"
                                :state="!$v.form.primary_contact.$invalid"
                                trim>
                        </b-form-input>
                    </b-form-group>
                </b-col>
                <b-col>
                    <b-form-group
                            id="fieldset-1"
                            description=""
                            label="Secondary Contact"
                            label-for="input-1"
                            :invalid-feedback="invalidFeedback"
                            :valid-feedback="validFeedback"
                    >
                        <b-form-input
                                id="input-1"
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
                                label-for="input-1"
                                :invalid-feedback="invalidFeedback"
                                :valid-feedback="validFeedback"
                        >
                            <b-input-group>
                                <b-form-input
                                        id="input-1"
                                        v-model="form.redirect_uris[index]"
                                        :state="!$v.form.redirect_uris.$each[index].$invalid"
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
                        id="checkbox-group-1"
                        v-model="form.scope"
                        :options="scopeOptions"
                        name="flavour-1"
                ></b-form-checkbox-group>
            </b-form-group>
            <b-form-group
                id="fieldset-1"
                description=""
                label="Domain"
                label-for="input-1"
                :invalid-feedback="invalidFeedback"
                :valid-feedback="validFeedback"
            >
                <b-form-input
                        id="input-1"
                        v-model="form.domain"
                        :state="!$v.form.domain.$invalid"
                        trim>
                </b-form-input>
            </b-form-group>
            <b-form-group
                id="fieldset-1"
                description=""
                label="Client URI"
                label-for="input-1"
                :invalid-feedback="invalidFeedback"
                :valid-feedback="validFeedback"
            >
                <b-form-input
                        id="input-1"
                        v-model="form.client_uri"
                        :state="!$v.form.client_uri.$invalid"
                        trim>
                </b-form-input>
            </b-form-group>
            <b-form-group
                id="fieldset-1"
                description=""
                label="Logo URI"
                label-for="input-1"
                :invalid-feedback="invalidFeedback"
                :valid-feedback="validFeedback"
            >
                <b-form-input
                        id="input-1"
                        v-model="form.logo_uri"
                        :state="!$v.form.logo_uri.$invalid"
                        trim>
                </b-form-input>
            </b-form-group>

            <b-form-group
                id="fieldset-1"
                description="(At least 15 characters long) Provide description of the new tenant and any other comments here."
                label="Comment"
                label-for="input-1"
                :invalid-feedback="invalidFeedback"
                :valid-feedback="validFeedback"
            >
                <b-form-textarea
                        rows="3"
                        textarea
                        id="input-1"
                        v-model="form.comment"
                        :state="!$v.form.comment.$invalid"
                        trim>
                </b-form-textarea>
            </b-form-group>
            <b-form-group label="Application Type">
                <b-form-radio-group
                    id="radio-group-1"
                    v-model="form.application_type"
                    :options="application_typeOptions"
                    name="radio-options"
                ></b-form-radio-group>
            </b-form-group>


            <b-button type="submit" variant="primary">Submit</b-button>


        </b-form>
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
                    application_type: "web",
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
                domain: {url},
                client_uri: {required},
                logo_uri: {url},
                application_type: {required},
                redirect_uris: {
                    $each:{
                        required, url
                        }
                },
                comment: {required, minLength: minLength(15)}
            }
        },
        methods: {
            onSubmit(event) {
                event.preventDefault();
                console.log(this.$v.form.client_name)
            },
            addRedirectUri: function () {
                this.form.redirect_uris.push("");
            },
            deleteRedirectUri: function (index) {
                console.log(index);
                this.form.redirect_uris.splice(index, 1);
            }
        }
    }
</script>