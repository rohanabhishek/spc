CREATE TABLE anuragChatalgho(`id` Int Unsigned Not Null Auto_Increment,
	                            `name` VarChar(255) Not Null Default 'Untitled.txt',
                                `mime` VarChar(50) Not Null Default 'text/plain',
                                `size` BigInt Unsigned Not Null Default 0,
                                `data` LongBlob Not Null,
                                `created` DateTime Not Null,
                                `md5sum` VarChar(40) Not Null,
                                PRIMARY KEY (`id`) );