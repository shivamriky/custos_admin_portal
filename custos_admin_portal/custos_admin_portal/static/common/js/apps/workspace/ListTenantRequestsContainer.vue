<template>
    <div>
        <div class="row">
            <div class="col">
                <h1 class="h4 mb-4">Existing Tenants Request</h1>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <div class="card">
                    <div class="card-body">
                        <table class="table table-hover">
                            <thead>
                            <tr>
                                <th>Request Id</th>
                                <th>Client Name</th>
                                <th>Creation Time</th>
                                <th>Status</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr
                                    v-for="tR in tenantRequests"
                                    :key="tR.requestId"
                            >
                                <td>
                                    <b-link @click="viewLink(tR)">{{tR.requestId}}</b-link>
                                </td>
                                <td>{{tR.clientName}}</td>
                                <td>
                                    <span>{{ tR.creationTime }}</span>
                                </td>
                                <td>
                                    {{tR.status}}
                                </td>
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


    import {now} from "moment";
    import urls from "./utils/urls";

    export default {

        data() {
            return {
                tenantRequests: []
            }
        },
        beforeMount() {
            this.tenantRequests.push({
                requestId: '234234324',
                clientName: 'scigap',
                creationTime: now(),
                status: 'Active'
            });
            this.tenantRequests.push({
                requestId: '54645645',
                clientName: 'scigap',
                creationTime: now(),
                status: 'Active'
            })
        },
        methods: {
            viewLink(tenantRequest) {
                console.log("Executed view link",tenantRequest)
                return urls.navigateToViewRequest(tenantRequest)
            }
        }
    };
</script>

<style>
</style>
